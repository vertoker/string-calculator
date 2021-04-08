using System.Collections.Generic;
using System;

static class Calculator
{
    #region Static readonly data
    private static readonly Dictionary<string, string> errors =
    {
        { "pluslarge", "The plus is too large to calculate" },
        { "minuslarge", "The minus is too large to calculate" },
        { "multiplylarge", "The multiply is too large to calculate" },
        { "divisionlarge", "The division is too large to calculate" },
        { "div0", "Can not be divided by zero" },
        { "degreelarge", "The degree is too large to calculate" },
        { "factminus", "Сan not calculate a factorial from a negative number" },
        { "factlarge", "The factorial is too large to calculate" },
        { "sqrtminus", "Сan not calculate the square root from a negative number" },
        { "nonums", "You broke real error protection. How?" }
    };
    private static readonly Dictionary<string, string> warnings =
    {
        { "null", "Expression is empty" },
        { "skipmultiply", "Skipped multiplication sign" },
        { "skipnumber", "Skipped number between/nearby sign(s)" },
        { "openparenthesis", "There is an extra open parenthesis" },
        { "closedparenthesis", "There is an extra closed parenthesis" },
        { "additionalpoint", "There is an extra dot in the number" },
        { "additionalsymbol", "There is an extra symbol in the expression, which not used in computation" }
    };
    private static readonly Dictionary<char, int> order_signs =
    { { '+', 1 }, { '-', 1 }, { '*', 2 }, { '/', 2 }, { '^', 3 }, { '√', 4 }, { '!', 5 } };
    private static readonly Dictionary<char, int> pos_types =
    { { '+', 0 }, { '-', 0 }, { '*', 0 }, { '/', 0 }, { '^', 0 }, { '√', 1 }, { '!', 2 } };
    private static readonly string all_nums_constants = ".1234567890epi";
    private static readonly string all_nums_point = ".1234567890";
    private static readonly string all_nums = "1234567890";
    private static readonly string all_operations = "+-*/^√!";
    private static readonly string type0_operations = "+-*/^";
    private static readonly string type1_operations_special = "√(";
    private static readonly string type2_operations_special = "!)";

    private static readonly char plus_operation = '+';
    private static readonly char minus_operation = '-';
    private static readonly char multiply_operation = '*';
    private static readonly char division_operation = '/';
    private static readonly char degree_operation = '^';
    private static readonly char type1_operation = '√';
    private static readonly char type2_operation = '!';
    private static readonly char open_parenthesis = '(';
    private static readonly char closed_parenthesis = ')';
    private static readonly char point = '.';
    private static readonly string pi = "pi";
    private static readonly char zero = '0';
    private static readonly char e = 'e';
    #endregion

    #region Calculate operations
    private static double Factorial(int num)
    {
        if (num < 2)
            return 1;
        return num * Factorial(num - 1);
    }
    private static int FindAllCount(string original, string substring)
    {
        int pos = 0, count = 0;
        while ((pos < original.Length) && (pos = original.IndexOf(substring, pos)) != -1)
        {
            pos += stringToFind.Length();
            count++;
        }

        foreach (var p in positions)
        {
            Console.WriteLine(p);
        }
    }
    private static double Operation(char sign, double num1, double num2)
    {
        try
        {
            switch (sign)
            {
                case '+': return num1 + num2;
                case '-': return num1 - num2;
                case '*': return num1 * num2;
                case '/': return num1 / num2;
                case '^': return Math.Pow(num1, num2);
                case '!': return Factorial(int.Parse(num1));
                case '√': return Math.Sqrt(num2);
                default: return 0;
            }
        }
        catch (Exception)
        {
            return 0;
        }
    }
    private static double Operation(char sign, double num1, double num2, ref string error = "")
    {
        switch (sign)
        {
            case '+':
                try
                {
                    return num1 + num2;
                }
                catch (Exception)
                {
                    error = errors["pluslarge"];
                    return 0;
                }
            case '-':
                try
                {
                    return num1 - num2;
                }
                catch (Exception)
                {
                    error = errors["minuslarge"];
                    return 0;
                }
            case '*':
                try
                {
                    return num1 * num2;
                }
                catch (Exception)
                {
                    error = errors["multiplylarge"];
                    return 0;
                }
            case '/':
                if (num2 == 0)
                {
                    error = errors["div0"];
                    return 0;
                }
                try
                {
                    return num1 / num2;
                }
                catch (Exception)
                {
                    error = errors["divisionlarge"];
                    return 0;
                }
            case '^':
                try
                {
                    return Math.Pow(num1, num2);
                }
                catch (Exception)
                {
                    error = errors["degreelarge"];
                    return 0;
                }
            case '!':
                if (num1 < 0)
                {
                    error = errors["factminus"];
                    return 0;
                }
                try
                {
                    return Factorial(int.Parse(num1));
                }
                catch (Exception)
                {
                    error = errors["factlarge"];
                    return 0;
                }
            case '√':
                if (num2 < 0)
                {
                    error = errors["sqrtminus"];
                    return 0;
                }
                try
                {
                    return Math.Sqrt(num2);
                }
                catch (Exception)
                {
                    error = errors["sqrtlarge"];
                    return 0;
                }
            default: return 0;
        }
    }
    #endregion

    public static double Calculate(string expression)
    {
        if (expression == string.Empty)
            return 0;

        // Format input
        expression = expression.ToLower();
        expression = expression.Replace(',', '.');
        expression = expression.Replace(':', '/');
        expression = expression.Replace('\\', '/');
        expression = expression.Replace("**", '^');

        // Temporarity params
        int length = expression.Length;
        List<string> stringNums = new List<string>();
        string localNum = string.Empty, num = string.Empty;
        int power = 0, targetNum = 0, nextError = 0;
        bool hasPoint, hasNums;
        double multiplier;

        // Lists (all return params)
        List<double> nums = new List<double>();
        List<char> signs = new List<char>();
        List<int> order = new List<int>();
        List<int> target = new List<int>();

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
            else if (s == type2_operation)//!
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
                        signs.Add('*');
                        order.Add(power);
                        target.Add(targetNum);
                        targetNum++;
                    }
                }
            }
            else if (s == type1_operation)//√
            {
                target.Add(targetNum);

                if (notFirstChar)
                {
                    if (all_nums_constants.Contains(expression[i - 1]))//.1234567890epi
                    {
                        signs.Add('*');
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
                        signs.Add('*');
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
                        signs.Add('*');
                        order.Add(power);
                        target.Add(targetNum);
                        targetNum++;
                    }
                }
            }
            else
            {
                localNum = localNum + s;
                isNum = true;
            }

            if (!isNum)
            {
                if (localNum != string.Empty && localNum != minus_operation)//-
                {
                    stringNums.Add(localNum);
                    localNum = string.Empty;
                }
            }
            if (nextError > 0)
            {
                for (int i = 0; i < nextError; i++)
                    stringNums.Add(zero);
                nextError = 0;
            }

            // Logs
            // Console.WriteLine();
        }

        // Checkout on error and other
        if (localNum != string.Empty && localNum != minus_operation)//-
            stringNums.Add(localNum);
        if (nextError > 0)
            for (int i = 0; i < length; i++)
                stringNums.Add(zero);
        if (stringNums.Count == 0)
            return 0;

        //Clean numbers and find constants
        for (int i = 0; i < stringNums.Count; i++)
        {
            num = stringNums[i];
            localNum = string.Empty;
            hasPoint = hasPoint = false;
            multiplier = 1;

            if (num.Contains(pi))
            {
                multiplier *= Math.Pow(Math.PI, FindAllCount(num, pi));
                num.Replace(pi, plus_operation);
                hasNums = true;
            }
            if (num.Contains(e))
            {
                multiplier *= Math.Pow(Math.E, FindAllCount(num, e));
                num.Replace(e, plus_operation);
                hasNums = true;
            }

            for (int n = 0; n < num; n++)
            {
                if (all_nums.Contains(num[n]))
                {
                    localNum = localNum + num[n];
                    hasNums = true;
                }
                else if (num[n] == point)
                {
                    if (!hasPoint)
                    {
                        localNum = localNum + num[n];
                        hasNums = hasPoint = true;
                    }
                }
                else if (localNum != string.Empty)
                {
                    if (localNum[0] == point)
                        localNum = zero + localNum;
                    if (localNum[localNum.Length - 1] == point)
                        localNum = localNum + zero;
                    multiplier *= double.Parse(localNum);
                    localNum = string.Empty;
                }
            }

            if (localNum != string.Empty)
            {
                if (localNum[0] == point)
                    localNum = zero + localNum;
                if (localNum[localNum.Length - 1] == point)
                    localNum = localNum + zero;
                multiplier *= double.Parse(localNum);
            }
            if (hasNums)
                nums[i] = multiplier;
            else
                nums[i] = 0;
        }

        // Calculate
        for (int i = 0; i < length; i++)
        {
            int nextID = 0;
            int signPower = order_signs[signs[0]];
            int signOrder = order[0];

            for (int j = 0; j < length; j++)
            {
                int localOrder = order[j];
                int localPower = order_signs[signs[j]];

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

            int posType = pos_types[signs[nextID]];
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