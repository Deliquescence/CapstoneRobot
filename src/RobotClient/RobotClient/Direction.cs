using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace RobotClient
{
    public class Direction
    {
        public readonly DateTime time;
        public readonly double throttle;
        public readonly double direction;

        private readonly static string[] ThrottleStrings = { "Moving backwards", "In Neutral", "Moving forwards" };
        private readonly static string[] DirectionStrings = { "and left", "", "and right" };

        public Direction(DateTime time, double throttle, double direction)
        {
            this.time = time;
            this.throttle = throttle;
            this.direction = direction;
        }

        /**
         * Parses a List of Directional data from the raw log string
         */
        public static List<Direction> ParseLog(string fullLogString)
        {
            var split = Regex.Split(fullLogString, "\n");
            return split.Where(line => line.Contains("@")).Select(line => ParseDirection(line)).ToList();
        }

        /**
         * Parses a single Directional command from a single line of the log file
         */
        public static Direction ParseDirection(string logString)
        {
            var split = logString.Split('@');
            split = split[1].Split(' ');
            var throttle = double.Parse(split[0]);
            var direction = double.Parse(split[1]);
            var time = DateTime.Parse(logString.Split('\t')[0]);
            return new Direction(time, throttle, direction);
        }

        /**
         * Encodes a directional command and its timestamp into log string format
         */
        public static string EncodeDirection(DateTime time, double throttleController, double directionController)
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
            var dt = time.ToString("MM/dd/yyyy hh:mm:ss.fff tt");
            return $"{dt}\t{ThrottleStrings[throttleIndex]} {DirectionStrings[directionIndex]}@{throttleController} {directionController} \n";
        }
    }
}
