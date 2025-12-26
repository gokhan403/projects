using System;
using System.Collections;

namespace gp
{
    class Example
    {
        public static void Main(string[] args)
        {
            Hashtable ht = new Hashtable();

            ht.Add("İstanbul", new string[] { "Arnavutköy", "Avcılar", "Bağcılar", "Bahçelievler", 
                                              "Bakırköy", "Bayrampaşa", "Başakşehir", "Beşiktaş", 
                                              "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çatalca", 
                                              "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", 
                                              "Gaziosmanpaşa", "Güngören", "Kağıthane", "Küçükçekmece", 
                                              "Sarıyer", "Silivri", "Sultangazi", "Şişli", 
                                              "Zeytinburnu", "Adalar", "Ataşehir", "Beykoz", 
                                              "Çekmeköy", "Kadıköy", "Kartal", "Maltepe", 
                                              "Pendik", "Sancaktepe", "Sultanbeyli", "Şile", 
                                              "Tuzla", "Ümraniye", "Üsküdar" });
            ht.Add("Edirne", new string[] { "Enez", "Havsa", "İpsala", "Keşan", "Lalapaşa",
                                            "Meriç", "Süloğlu", "Uzunköprü" });
            ht.Add("Kırklareli", new string[] { "Babaeski", "Demirköy", "Kofçaz", "Lüleburgaz",
                                                "Pehlivanköy", "Pınarhisar", "Vize" });
            ht.Add("Tekirdağ", new string[] { "Süleymanpaşa", "Çerkezköy", "Çorlu", "Ergene",
                                              "Hayrabolu", "Kapaklı", "Malkara", "Marmaraeğrelisi", 
                                              "Muratlı", "Saray", "Şarköy" });
            ht.Add("Çanakkale", new string[] { "Ayvacık", "Bayramiç", "Biga", "Bozcaada", 
                                               "Çan", "Eceabat", "Ezine", "Gelibolu", 
                                               "Gökçeada", "Lapseki", "Yenice" });
            ht.Add("Kocaeli", new string[] { "Başiskele", "İzmit", "Kartepe", "Derince", 
                                             "Gölcük", "Körfez", "Çayırova", "Darıca", 
                                             "Dilovası", "Gebze", "Kandıra", "Karamürsel" });
            ht.Add("Yalova", new string[] { "Altınova", "Armutlu", "Çınarcık", "Çiftlikköy",
                                            "Termal" });
            ht.Add("Sakarya", new string[] { "Adapazarı", "Arifiye", "Erenler", "Serdivan", 
                                             "Akyazı", "Ferizli", "Gevye", "Hendek", 
                                             "Karapürçek", "Karasu", "Kaynarca", "Kocaali", 
                                             "Pamukova", "Sapanca", "Söğütlü", "Taraklı" });
            ht.Add("Bilecik", new string[] { "Bozüyük", "Gölpazarı", "İnhisar", "Osmaneli", 
                                             "Pazaryeri", "Söğüt", "Yenipazar" });
            ht.Add("Bursa", new string[] { "Gürsu", "Kestel", "Nilüfer", "Osmangazi", 
                                           "Yıldırım", "Büyükorhan", "Gemlik", "Harmancık", 
                                           "İnegöl", "İznik", "Karacabey", "Keles", 
                                           "Mudanya", "Mustafakemalpaşa", "Orhaneli", "Orhangazi", 
                                           "Yenişehir" });
            ht.Add("Balıkesir", new string[] { "Altıeylül", "Karesi", "Ayvalık", "Balya", 
                                               "Bandırma", "Bigadiç", "Burhaniye", "Dursunbey", 
                                               "Edremit", "Erdek", "Gömeç", "Gönen", 
                                               "Havran", "İvrindi", "Kepsut", "Manyas", 
                                               "Marmara", "Savaştepe", "Sındırgı", "Susurluk" });
            
            string? sehir;
            Console.Write("Marmara bölgesinde bulunan bir şehir ismi giriniz: ");
            sehir = Console.ReadLine();

            object ilceObject = ht[sehir];
            if (ht.ContainsKey(sehir))
            {
                if (ilceObject is string[])
                {
                    string[] sehirIlce = (string[])ilceObject;
                    Console.WriteLine("Şehrin ilçeleri: ");
                    foreach (string s in sehirIlce)
                        Console.Write(s + " - ");
                }
            }
            else
            {
                Console.WriteLine("Yanlış şehir ismi girdiniz!");
            }

        }
    }
}
