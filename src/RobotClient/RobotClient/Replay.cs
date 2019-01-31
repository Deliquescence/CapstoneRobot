using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace RobotClient
{
    public class Replay
    {
        private PiCarConnection piCar;
        private Thread replayThread;
        private List<Tuple<TimeSpan, Direction>> savedOffsetInputs;


        /**
         * Given two different car connections and a list of inputs,
         * start replaying to the first car and then replay to the second car after a delay.
         */
        public static Tuple<Replay, Replay> StartTwoWithDelay(PiCarConnection first, PiCarConnection second, List<Direction> savedInputs, TimeSpan delay)
        {
            var firstReplay = new Replay(first, savedInputs);
            var secondReplay = new Replay(second, savedInputs);

            firstReplay.Start();

            Thread.Sleep(delay);
            secondReplay.Start();

            return Tuple.Create(firstReplay, secondReplay);
        }

        /**
         * Given two different car connections and a list of inputs,
         * start replaying to the first car and then replay to the second car after giving an initial forward acceleration.
         * This is done in order to catch up to the starting position of the first car.
         */
        public static Tuple<Replay, Replay> StartTwoWithCatchup(PiCarConnection first, PiCarConnection second, List<Direction> savedInputs, double catchupDistance)
        {
            TimeSpan CatchupDuration = TimeSpan.FromSeconds(catchupDistance / PiCarConnection.SPEED_AT_MAX_THROTTLE);

            var secondInputs = new List<Direction>(savedInputs);
            Direction catchupInput = new Direction(secondInputs[0].time - CatchupDuration, 1.0, 0.0);
            secondInputs.Insert(0, catchupInput);
            secondInputs.Add(new Direction(secondInputs.Last().time, 0.0, 0.0)); // Ensure we stop at the end

            Direction avoidCrashInput = new Direction(savedInputs.Last().time, 1.0, 0.0);
            savedInputs.Add(avoidCrashInput);
            savedInputs.Add(new Direction(savedInputs.Last().time + CatchupDuration, 0.0, 0.0)); // Stop after avoiding crash

            var firstReplay = new Replay(first, savedInputs);
            var secondReplay = new Replay(second, secondInputs);

            firstReplay.Start();
            secondReplay.Start();

            return Tuple.Create(firstReplay, secondReplay);
        }

        /**
         * Create a replay which will send the SavedInputs to the piCar after .Start() is called.
         */
        public Replay(PiCarConnection piCarConnection, List<Direction> savedInputs)
        {
            this.piCar = piCarConnection;

            // Map Direction -> <Offset to next instruction, Direction>
            var priorTime = savedInputs[0].time;
            this.savedOffsetInputs = savedInputs.Select(x =>
            {
                var t = Tuple.Create(x.time - priorTime, x);
                if (t.Item1.Duration() != t.Item1) {
                    throw new ArgumentException("Replay inputs must be in chronological order");
                }
                priorTime = x.time;
                return t;
            }).ToList();
            this.replayThread = new Thread(DoReplay);
        }

        private void DoReplay()
        {
            try
            {
                foreach (var x in savedOffsetInputs)
                {
                    Thread.Sleep(x.Item1);
                    piCar.SetMotion(x.Item2.throttle, x.Item2.direction);
                }
            }
            catch (ThreadAbortException)
            {
                Console.Write("Replay was aborted");
            }
        }

        /**
         * Begin sending the saved inputs to the car.
         */
        public void Start()
        {
            this.replayThread.Start();
        }

        /**
         * Stop sending inputs to the car.
         * The replay cannot be restarted after doing this.
         */
        public void Stop()
        {
            this.replayThread.Abort();
        }

        /**
         * Return true if this replay has been started and is still ongoing.
         */
        public bool isActive()
        {
            return this.replayThread.IsAlive;
        }

    }
}
