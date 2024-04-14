using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        // programda kullan�lacak sabit de�er ve de�i�kenler
        private int buttonWidth = 100;
        private int buttonHeight = 100;
        private Button m_emptyButton;
        private int[] m_array = new int[24];
        public Form1()
        {
            InitializeComponent();
            // pencere ad� ve boyutlar� girilir
            this.Text = "Buton Kayd�rmaca Oyunu";
            this.ClientSize = new Size(buttonWidth * 5, buttonHeight * 5);

            // pencere boyutlar� de�i�ti�inde buton boyutlar�n�n
            // uygun �ekilde �l�eklenmesi sa�lan�r
            this.Resize += new EventHandler(resizeHandler);

            // butonlar bir arkaplan rengi ve
            // uygun say�lar ile kar���k �ekilde pencerede
            // olu�turulur, bir bo�luk b�rak�l�r
            int x, y = 0;
            Color color = Color.FromArgb(138, 167, 188);
            for(int i = 0; i < 5; i++)
            {
                x = 0;
                for(int j = 0; j < 5; j++)
                {
                    if (x == 200 && y == 200) // pencerenin ortas�nda bo�luk
                    {
                        m_emptyButton = new Button();
                        m_emptyButton.Bounds = new Rectangle(x, y, buttonWidth, buttonHeight);
                        this.Controls.Add(m_emptyButton);
                        x += buttonWidth;
                        continue;
                    }

                    Button button = new Button();
                    button.Bounds = new Rectangle(x, y, buttonWidth, buttonHeight);
                    button.BackColor = color;

                    // say�lar�n kar���k yerle�mesi sa�lan�r
                    Random random = new Random();
                    int randomInt;
                    while (true)
                    {
                        randomInt = random.Next(1, 25);
                        if (m_array[randomInt - 1] == 1)
                            continue;
                        else
                        {
                            m_array[randomInt - 1]++;
                            break;
                        }
                    }
                    button.Text = string.Format("{0}", randomInt);
                    // uygun butona bas�ld���nda yer de�i�tirmesi sa�lan�r
                    button.Click += new EventHandler(clickHandler); 
                    this.Controls.Add(button);
                    x += buttonWidth;
                }
                y += buttonHeight;
            }
        }

        // butonu yer de�i�tirmek i�in metod
        private void clickHandler(object sender, EventArgs e)
        {
            // butona bas�ld���nda butonun koordinatlar� al�n�r ve
            // e�er uygun butona bas�ld�ysa buton ve bo�luk yer de�i�tirir
            Button button = (Button) sender;
            if((button.Location.X == m_emptyButton.Location.X - buttonWidth && button.Location.Y == m_emptyButton.Location.Y) ||
               (button.Location.X == m_emptyButton.Location.X + buttonWidth && button.Location.Y == m_emptyButton.Location.Y) ||
               (button.Location.Y == m_emptyButton.Location.Y - buttonHeight && button.Location.X == m_emptyButton.Location.X) ||
               (button.Location.Y == m_emptyButton.Location.Y + buttonHeight && button.Location.X == m_emptyButton.Location.X))
            {
                Point temp = new Point();
                temp = m_emptyButton.Location;
                m_emptyButton.Location = button.Location;
                button.Location = temp;
            }
        }
        
        // butonlar� uygun �ekilde �l�ekleyecek metod
        private void resizeHandler(object sender, EventArgs e)
        {
            // pencere boyutu de�i�ti�inde yeni boyutlar�n
            // butonlara uygun oran� al�n�r
            buttonWidth = this.ClientSize.Width / 5;
            buttonHeight = this.ClientSize.Height / 5;

            // yeni boyutlar ile butonlar tekrar yazd�r�l�r
            int x, y = 0;
            for(int i = 0; i < 5; i++)
            {
                x = 0;
                for(int j = 0; j < 5; j++)
                {
                    this.Controls[i * 5 + j].Location = new Point(x, y);
                    this.Controls[i * 5 + j].Size = new Size(buttonWidth, buttonHeight);

                    x += buttonWidth;
                }
                y += buttonHeight;
            }
        }
        
    }
}
