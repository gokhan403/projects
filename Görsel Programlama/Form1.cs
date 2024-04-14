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
        // programda kullanýlacak sabit deðer ve deðiþkenler
        private int buttonWidth = 100;
        private int buttonHeight = 100;
        private Button m_emptyButton;
        private int[] m_array = new int[24];
        public Form1()
        {
            InitializeComponent();
            // pencere adý ve boyutlarý girilir
            this.Text = "Buton Kaydýrmaca Oyunu";
            this.ClientSize = new Size(buttonWidth * 5, buttonHeight * 5);

            // pencere boyutlarý deðiþtiðinde buton boyutlarýnýn
            // uygun þekilde ölçeklenmesi saðlanýr
            this.Resize += new EventHandler(resizeHandler);

            // butonlar bir arkaplan rengi ve
            // uygun sayýlar ile karýþýk þekilde pencerede
            // oluþturulur, bir boþluk býrakýlýr
            int x, y = 0;
            Color color = Color.FromArgb(138, 167, 188);
            for(int i = 0; i < 5; i++)
            {
                x = 0;
                for(int j = 0; j < 5; j++)
                {
                    if (x == 200 && y == 200) // pencerenin ortasýnda boþluk
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

                    // sayýlarýn karýþýk yerleþmesi saðlanýr
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
                    // uygun butona basýldýðýnda yer deðiþtirmesi saðlanýr
                    button.Click += new EventHandler(clickHandler); 
                    this.Controls.Add(button);
                    x += buttonWidth;
                }
                y += buttonHeight;
            }
        }

        // butonu yer deðiþtirmek için metod
        private void clickHandler(object sender, EventArgs e)
        {
            // butona basýldýðýnda butonun koordinatlarý alýnýr ve
            // eðer uygun butona basýldýysa buton ve boþluk yer deðiþtirir
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
        
        // butonlarý uygun þekilde ölçekleyecek metod
        private void resizeHandler(object sender, EventArgs e)
        {
            // pencere boyutu deðiþtiðinde yeni boyutlarýn
            // butonlara uygun oraný alýnýr
            buttonWidth = this.ClientSize.Width / 5;
            buttonHeight = this.ClientSize.Height / 5;

            // yeni boyutlar ile butonlar tekrar yazdýrýlýr
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
