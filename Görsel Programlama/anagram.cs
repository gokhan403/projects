using System;
using System.Collections;
using System.Data;

namespace gp
{
    class Example
    {
        public static void Main(string[] args)
        {
            Hashtable ht = new Hashtable();

            string? str1;
            string? str2;
            Console.Write("Birinci kelimeyi giriniz: ");
            str1 = Console.ReadLine();
            Console.Write("İkinici kelimeyi giriniz: ");
            str2 = Console.ReadLine();

            for(int i = 0; i < str1.Length; i++)
            {
                if (ht.ContainsKey(str1[i]))
                {
                    int value = (int)ht[str1[i]];
                    value++;
                    ht[str1[i]] = value;
                }
                else
                {
                    ht.Add(str1[i], 1);
                }
            }

            for(int i = 0; i < str2.Length; i++)
            {
                if (!ht.ContainsKey(str2[i]) || (int)ht[str2[i]] < 0)
                {
                    Console.WriteLine("Girdiğiniz kelimeler anagram değildir!");
                    return;
                }
                else
                {
                    int value = (int)ht[str2[i]];
                    value--;
                    ht[str2[i]] = value;
                }
            }

            Console.WriteLine("Girdiğiniz kelimeler anagramdır!");

        }
    }
}
