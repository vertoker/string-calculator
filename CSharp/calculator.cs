using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;
using System;

namespace ConsoleCalculator
{
    using num = System.Double;
    using order = System.Byte;
    using pos = System.Int16;

    static class Calculator
    {
        #region Const strings
        private const string all_nums_constants = ".1234567890epi";
        private const string all_nums_point = ".1234567890";
        private const string all_nums = "1234567890";

        private const string all_operations = "+-*/^√!";
        private const string type0_operations = "+-*/^";
        private const string type1_operations_special = "√(";
        private const string type2_operations_special = "!)";

        private const char plus_operation = '+';
        private const string plus_operation_string = "+";
        private const char minus_operation = '-';
        private const string minus_operation_string = "-";
        private const char multiply_operation = '*';
        private const string multiply_operation_string = "*";
        private const char division_operation = '/';
        private const string division_operation_string = "/";
        private const char degree_operation = '^';
        private const string degree_operation_string = "^";
        private const char sqrt_operation = '√';
        private const string sqrt_operation_string = "√";
        private const char fact_operation = '!';
        private const string fact_operation_string = "!";
        private const char open_parenthesis = '(';
        private const char closed_parenthesis = ')';
        private const char point = '.';
        private const char comma = ',';
        private const string pi = "pi";
        private const char zero = '0';
        private const string zero_string = "0";
        private const char e = 'e';
        #endregion

        #region Static readonly data
        private delegate num OperationDelegate(num num1, num num2);

        private static readonly Dictionary<char, OperationDelegate> operations = new Dictionary<char, OperationDelegate>()
        {
            { minus_operation, (num num1, num num2) => { return num1 - num2; } },
            { plus_operation, (num num1, num num2) => { return num1 + num2; } },
            { multiply_operation, (num num1, num num2) => { return num1 * num2; } },
            { division_operation, (num num1, num num2) => { return num1 / num2; } },
            { fact_operation, (num num1, num num2) => { return Factorial((int)num1); } },
            { sqrt_operation, (num num1, num num2) => { return Math.Sqrt(num2); } }
        };
        private static readonly Dictionary<char, order> order_signs = new Dictionary<char, order>()
        { 
            { plus_operation, 1 },
            { minus_operation, 1 },
            { multiply_operation, 2 },
            { division_operation, 2 },
            { degree_operation, 3 },
            { sqrt_operation, 4 },
            { fact_operation, 5 }
        };
        private static readonly Dictionary<char, pos> pos_types = new Dictionary<char, pos>()
        {
            { plus_operation, 0 },
            { minus_operation, 0 },
            { multiply_operation, 0 },
            { division_operation, 0 },
            { degree_operation, 0 },
            { sqrt_operation, 1 },
            { fact_operation, 2 }
        };
        #endregion

        #region Calculate operations
        private static num Factorial(int num)
        {
            if (num < 2)
                return 1;
            return num * Factorial(num - 1);
        }
        private static num Operation(char sign, num num1, num num2)
        {
            return operations[sign].Invoke(num1, num2);
        }
        #endregion

        public static num Calculate(string expression)
        {
            if (expression == string.Empty)
                return 0;

            // Format input
            expression = expression.ToLower();
            expression = expression.Replace(point, comma);
            expression = expression.Replace(':', division_operation);
            expression = expression.Replace('\\', division_operation);
            expression = expression.Replace("**", "^");

            // Temporarity params
            int length = expression.Length;
            List<string> stringNums = new List<string>();
            string localNum = string.Empty, num = string.Empty;
            pos power = 0;
            pos targetNum = 0;
            order nextError = 0;
            bool hasPoint, hasNums = false;
            double multiplier;

            // Lists (all return params)
            List<num> nums = new List<num>();
            List<char> signs = new List<char>();
            List<pos> order = new List<pos>();
            List<pos> target = new List<pos>();

            // Collect data and write lists
            for (int i = 0; i < length; i++)
            {
                char s = expression[i];
                bool isNum = false;
                bool notFirstChar = i > 0;
                bool notLastChar = i + 1 < length;

                if (type0_operations.Contains(s))//+-*/^
                {
                    target.Add(targetNum);
                    targetNum++;

                    if (notFirstChar)
                    {
                        bool numsBool = all_nums_constants.Contains(expression[i - 1]);//.1234567890epi
                        bool type2Bool = type2_operations_special.Contains(expression[i - 1]);//√(
                        if (!numsBool && !type2Bool)
                            nextError++;
                    }
                    else
                        nextError++;

                    if (notLastChar)
                    {
                        bool numsBool = all_nums_constants.Contains(expression[i + 1]);//.1234567890epi
                        bool type1Bool = type1_operations_special.Contains(expression[i + 1]);//!)
                        if (!numsBool && !type1Bool)
                            nextError++;
                    }
                    else
                        nextError++;

                    signs.Add(s);
                    order.Add(power);
                }
                else if (s == fact_operation)//!
                {
                    target.Add(targetNum);
                    signs.Add(s);
                    order.Add(power);

                    if (notFirstChar)
                    {
                        bool numsBool = all_nums_constants.Contains(expression[i - 1]);//.1234567890epi
                        bool type2Bool = type2_operations_special.Contains(expression[i - 1]);//!
                        if (!numsBool && !type2Bool)
                            nextError++;
                    }
                    else
                        nextError++;

                    if (notLastChar)
                    {
                        if (all_nums_constants.Contains(expression[i + 1]))//.1234567890epi
                        {
                            signs.Add(multiply_operation);
                            order.Add(power);
                            target.Add(targetNum);
                            targetNum++;
                        }
                    }
                }
                else if (s == sqrt_operation)//√
                {
                    target.Add(targetNum);

                    if (notFirstChar)
                    {
                        if (all_nums_constants.Contains(expression[i - 1]))//.1234567890epi
                        {
                            signs.Add(multiply_operation);
                            order.Add(power);
                            targetNum++;
                            target.Add(targetNum);
                        }
                    }

                    if (notLastChar)
                    {
                        bool numsBool = all_nums_constants.Contains(expression[i + 1]);//.1234567890epi
                        bool type1Bool = type1_operations_special.Contains(expression[i + 1]);//√
                        if (!numsBool && !type1Bool)
                            nextError++;
                    }
                    else
                        nextError++;

                    signs.Add(s);
                    order.Add(power);
                }
                else if (s == open_parenthesis)//(
                {
                    if (notFirstChar)
                    {
                        if (all_nums_constants.Contains(expression[i - 1]))//.1234567890epi
                        {
                            signs.Add(multiply_operation);
                            order.Add(power);
                            target.Add(targetNum);
                            targetNum++;
                        }
                    }

                    if (!notLastChar)
                        nextError++;

                    power++;
                }
                else if (s == closed_parenthesis)//)
                {
                    power--;

                    if (notFirstChar)
                    {
                        if (s == open_parenthesis)
                            nextError++;
                    }
                    else
                        nextError++;

                    if (notLastChar)
                    {
                        if (all_nums_constants.Contains(expression[i - 1]))//.1234567890epi
                        {
                            signs.Add(multiply_operation);
                            order.Add(power);
                            target.Add(targetNum);
                            targetNum++;
                        }
                    }
                }
                else
                {
                    localNum += s;
                    isNum = true;
                }

                if (!isNum)
                {
                    if (localNum != string.Empty && localNum != minus_operation_string)//-
                    {
                        stringNums.Add(localNum);
                        localNum = string.Empty;
                    }
                }
                if (nextError > 0)
                {
                    for (order j = 0; j < nextError; j++)
                        stringNums.Add(zero_string);
                    nextError = 0;
                }

                // Logs
                // Console.WriteLine();
            }

            // Checkout on error and other
            if (localNum != string.Empty && localNum != minus_operation_string)//-
                stringNums.Add(localNum);
            if (nextError > 0)
                for (int i = 0; i < length; i++)
                    stringNums.Add(zero_string);
            if (stringNums.Count == 0)
                return 0;

            length = stringNums.Count;
            //Clean numbers and find constants
            for (int i = 0; i < length; i++)
            {
                num = stringNums[i];
                localNum = string.Empty;
                hasPoint = hasPoint = false;
                multiplier = 1;

                if (num.Contains(pi))
                {
                    multiplier *= Math.Pow(Math.PI, Regex.Matches(num, pi).Count);
                    num.Replace(pi, plus_operation_string);
                    hasNums = true;
                }
                if (num.Contains(e))
                {
                    multiplier *= Math.Pow(Math.E, num.Count(x => x == e));
                    num.Replace(e, plus_operation);
                    hasNums = true;
                }

                int lengthNum = num.Length;
                for (int n = 0; n < lengthNum; n++)
                {
                    if (all_nums.Contains(num[n]))
                    {
                        localNum += num[n];
                        hasNums = true;
                    }
                    else if (num[n] == comma)
                    {
                        if (!hasPoint)
                        {
                            localNum += num[n];
                            hasNums = hasPoint = true;
                        }
                    }
                    else if (localNum != string.Empty)
                    {
                        if (localNum[0] == comma)
                            localNum = zero + localNum;
                        if (localNum[^1] == comma)
                            localNum += zero;
                        multiplier *= double.Parse(localNum);
                        localNum = string.Empty;
                    }
                }

                if (localNum != string.Empty)
                {
                    if (localNum[0] == comma)
                        localNum = zero + localNum;
                    if (localNum[^1] == comma)
                        localNum += zero;
                    multiplier *= double.Parse(localNum);
                }
                nums.Add(hasNums ? multiplier : 0);
            }

            // Calculate
            for (pos i = 0; i < signs.Count; i++)
            {
                pos nextID = 0;
                pos signPower = order_signs[signs[0]];
                pos signOrder = order[0];

                for (pos j = 1; j < signs.Count; j++)
                {
                    pos localOrder = order[j];
                    pos localPower = order_signs[signs[j]];

                    bool orderPriority = signOrder < localOrder;
                    bool signPriority = signPower < localPower;
                    bool degPriority = signPower == order_signs[degree_operation];
                    bool degLocPriority = localPower == order_signs[degree_operation];
                    if (orderPriority || signOrder == localOrder && (signPriority || degPriority && degLocPriority))
                    {
                        nextID = j;
                        signPower = localPower;
                        signOrder = localOrder;
                    }
                }

                pos posType = pos_types[signs[nextID]];
                if (posType == 0)
                {
                    nums[target[nextID]] = Operation(signs[nextID], nums[target[nextID]], nums[target[nextID] + 1]);
                    int last = target[nextID];
                    signs.RemoveAt(nextID);
                    order.RemoveAt(nextID);
                    nums.RemoveAt(target[nextID] + 1);
                    target.RemoveAt(nextID);
                    for (int j = 0; j < target.Count; j++)
                        if (target[j] > last)
                            target[j]--;
                }
                else if (posType == 1)
                {
                    nums[target[nextID]] = Operation(signs[nextID], 0, nums[target[nextID]]);
                    if (target[nextID] + 1 < nums.Count && signs.Count < nums.Count)
                    {
                        nums[target[nextID]] = Operation(multiply_operation, nums[target[nextID]], nums[target[nextID] + 1]);
                        nums.RemoveAt(target[nextID] + 1);
                    }
                    signs.RemoveAt(nextID);
                    order.RemoveAt(nextID);
                    target.RemoveAt(nextID);
                }
                else if (posType == 2)
                {
                    nums[target[nextID]] = Operation(signs[nextID], nums[target[nextID]], 0);
                    signs.RemoveAt(nextID);
                    order.RemoveAt(nextID);
                    target.RemoveAt(nextID);
                }
            }
            return nums[0];
        }
    }
}