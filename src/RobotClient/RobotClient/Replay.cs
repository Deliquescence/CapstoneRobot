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

        public void Start()
        {
            this.replayThread.Start();
        }

        public void Stop()
        {
            this.replayThread.Abort();
        }

    }
}
