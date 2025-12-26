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
            
            string? str;
            Console.Write("Bir kelime giriniz: ");
            str = Console.ReadLine();

            for(int i = 0; i < str.Length; i++)
            {
                if (ht.ContainsKey(str[i]))
                {
                    Console.WriteLine("Bu kelimenin bütün harfleri farklı değil!");
                    return;
                }
                else
                {
                    ht.Add(str[i], null);
                }
            }

            Console.WriteLine("Bu kelimenin bütün harfleri farklı!");

        }
    }
}
