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
        private List<Direction> savedInputs;


        /**
         * Given two different car connections and a list of inputs,
         * start replaying to the first car and then replay to the second car after a delay.
         */
        public static Tuple<Replay, Replay> StartTwoWithDelay(PiCarConnection first, PiCarConnection second, List<Direction> SavedInputs, TimeSpan delay)
        {
            var firstReplay = new Replay(first, SavedInputs);
            var secondReplay = new Replay(second, SavedInputs);

            firstReplay.Start();

            Thread.Sleep(delay);
            secondReplay.Start();

            return Tuple.Create(firstReplay, secondReplay);
        }

        /**
         * Create a replay which will send the SavedInputs to the piCar after .Start() is called.
         */
        public Replay(PiCarConnection piCarConnection, List<Direction> SavedInputs)
        {
            this.piCar = piCarConnection;
            this.savedInputs = SavedInputs;
            this.replayThread = new Thread(DoReplay);
        }

        private void DoReplay()
        {
            var logBeginTime = savedInputs[0].time;
            var replayBeginTime = DateTime.Now;

            try
            {
                while (savedInputs.Any())
                {
                    var logElapsed = savedInputs[0].time - logBeginTime;
                    var replayElapsed = DateTime.Now - replayBeginTime;

                    if (logElapsed <= replayElapsed)
                    {
                        piCar.SetMotion(savedInputs[0].throttle, savedInputs[0].direction);
                        savedInputs.RemoveAt(0);
                    }
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

    }
}
