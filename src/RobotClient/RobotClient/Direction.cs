using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RobotClient
{
    static class Direction
    {
        private readonly static string[] ThrottleStrings = { "Moving backwards", "In Neutral", "Moving forwards" };
        private readonly static string[] DirectionStrings = { "and left", "", "and right" };

        public static string EncodeDirection(double throttleController, double directionController)
        {
            int throttleIndex = 1;
            int directionIndex = 1;
            if (throttleController > 0)
            {
                throttleIndex = (int)Math.Ceiling(throttleController) + 1;
            }
            else if (throttleController < 0)
            {
                throttleIndex = (int)Math.Floor(throttleController) + 1;
            }

            if (directionController > 0)
            {
                directionIndex = (int)Math.Ceiling(directionController) + 1;
            }
            else if (directionController < 0)
            {
                directionIndex = (int)Math.Floor(directionController) + 1;
            }
            return DateTime.Now.ToString("MM/dd/yyyy hh:mm:ss.fff tt") + $":\t{ThrottleStrings[throttleIndex]} {DirectionStrings[directionIndex]}\n";
        }

        //public static Tuple<DateTime, double, double> DecodeDirection()
        //{

        //}
    }
}
