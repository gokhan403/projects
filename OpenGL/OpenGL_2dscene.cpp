#include <glad/glad.h>
#include <GLFW/glfw3.h>
#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <learnopengl/filesystem.h>
#include <learnopengl/shader_s.h>
#include <ft2build.h>
#include FT_FREETYPE_H
#include <iostream>
#include <map>
#include <string.h>

void RenderText(Shader &shader, std::string text, float x, float y, float scale, glm::vec3 color);

// pencere boyutlarý
const unsigned int width = 800;
const unsigned int height = 600;

// yüklenen karakterlerin durum bilgisi tutulur
struct Character
{
	unsigned int TextureID;
	glm::ivec2   Size;
	glm::ivec2   Bearing;
	unsigned int Advance;
};

std::map<char, Character> Characters;
unsigned int textVAO, textVBO;

int main()
{
	// opengl aktifleþtirilir ve versiyon belirlenir
	glfwInit();

	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	// sahnede bulunan objelerin ve her objenin texturelarýnýn
	// koordinatlarý
	GLfloat verticesScene[] =
	{
		 // koordinatlar	  // renkler	       // doku
		-0.5f, -0.5f, 0.0f,   1.0f, 0.0f, 0.0f,   -1.0f, -1.0f,
		-0.5f,  0.4f, 0.0f,   1.0f, 0.0f, 0.0f,   -1.0f,  0.0f,
		 0.5f,  0.4f, 0.0f,	  1.0f, 0.0f, 0.0f,    0.0f,  0.0f,
		 0.5f, -0.5f, 0.0f,	  1.0f, 0.0f, 0.0f,    0.0f, -1.0f
	};

	GLfloat verticesMoon[] =
	{
		// koordinatlar		    // renkler	         // doku
		-0.45f,  0.45f, 0.0f,   1.0f, 0.0f, 0.0f,   -1.0f, -1.0f,
		-0.45f,  0.6f,  0.0f,   1.0f, 0.0f, 0.0f,   -1.0f,  0.0f,
		-0.3f,   0.6f,  0.0f,   1.0f, 0.0f, 0.0f,    0.0f,  0.0f,
		-0.3f,   0.45f, 0.0f,   1.0f, 0.0f, 0.0f,    0.0f, -1.0f
	};

	GLfloat verticesMan[] =
	{
		 // koordinatlar		 // renkler	         // doku
		 0.07f, -0.13f, 0.01f,   1.0f, 0.0f, 0.0f,   -1.0f, -1.0f,
		 0.07f,  0.08f, 0.01f,   1.0f, 0.0f, 0.0f,   -1.0f,  0.0f,
		-0.03f,  0.08f, 0.01f,   1.0f, 0.0f, 0.0f,    0.0f,  0.0f,
		-0.03f, -0.13f, 0.01f,   1.0f, 0.0f, 0.0f,    0.0f, -1.0f
	};

	GLfloat verticesGrass[] =
	{
		 // koordinatlar		 // renkler	         // doku
		 0.13f,  0.07f,  0.1f,   1.0f, 0.0f, 0.0f,   -1.0f, -1.0f,
		 0.13f,  0.15f, 0.1f,    1.0f, 0.0f, 0.0f,   -1.0f,  0.0f,
		 0.03f,  0.15f, 0.1f,	 1.0f, 0.0f, 0.0f,    0.0f,  0.0f,
		 0.03f,  0.07f,  0.1f,	 1.0f, 0.0f, 0.0f,    0.0f, -1.0f
	};

	GLfloat verticesCat[] =
	{
		// koordinatlar		     // renkler	         // doku
		-0.07f,  0.21f,  0.1f,   1.0f, 0.0f, 0.0f,   -1.0f, -1.0f,
		-0.07f,  0.29f,  0.1f,   1.0f, 0.0f, 0.0f,   -1.0f,  0.0f,
		-0.03f,  0.29f,  0.1f,   1.0f, 0.0f, 0.0f,    0.0f,  0.0f,
		-0.03f,  0.21f,  0.1f,   1.0f, 0.0f, 0.0f,    0.0f, -1.0f
	};
	
	GLfloat verticesText[] =
	{
		// koordinatlar		     // renkler	         // doku
		-0.2f ,  0.4f,  0.1f,   0.0f, 1.0f, 0.0f,   -1.0f, -1.0f,
		-0.2f,   0.5f,  0.1f,   0.0f, 1.0f, 0.0f,   -1.0f,  0.0f,
		 0.2f,   0.5f,  0.1f,   0.0f, 1.0f, 0.0f,    0.0f,  0.0f,
		 0.2f,   0.4f,  0.1f,   0.0f, 1.0f, 0.0f,    0.0f, -1.0f
	};
	
	// sahnedeki objeler üçgen cisimler olarak çizilir
	// bu üçgenlerin çizim indisleri
	GLuint indices[] =
	{
		0, 1, 2,
		0, 2, 3,
	};
	
	// opengl penceresi oluþturulur
	GLFWwindow* window = glfwCreateWindow(width, height, "OpenGL Lab3", NULL, NULL);
	if(window == NULL)
	{
		std::cout << "Failed to create GLFW window!" << std::endl;

		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);

	// opengl fonksiyonlarý yüklenir ve 
	//koordinat sisteminin pencerede nereden baþlayacaðý atanýr
	gladLoadGL();
	glViewport(0, 0, width, height);

	// renk harmanlama
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	// text renderlama için shader oluþturulur
	Shader shaderText("text.vert", "text.frag");
	glm::mat4 projText = glm::ortho(0.0f, static_cast<float>(width), 0.0f, static_cast<float>(height));
	shaderText.use();
	glUniformMatrix4fv(glGetUniformLocation(shaderText.ID, "projText"), 1, GL_FALSE, glm::value_ptr(projText));

	// shader programý oluþturulur
	Shader shaderProgram("default.vert", "default.frag");

	// bufferlar oluþturulur ve baðlanýr
	GLuint VAO1, VBO1, EBO1,
		   VAO2, VBO2, EBO2,
		   VAO3, VBO3, EBO3,
		   VAO4, VBO4, EBO4,
		   VAO5, VBO5, EBO5;

	glGenVertexArrays(1, &VAO1);
	glGenBuffers(1, &VBO1);
	glGenBuffers(1, &EBO1);
	glBindVertexArray(VAO1);
	glBindBuffer(GL_ARRAY_BUFFER, VBO1);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesScene), verticesScene, GL_STATIC_DRAW);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO1);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	// pozisyon baþlangýcý
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	// renk baþlangýcý
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);
	// doku koordinatý baþlangýcý
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
	glEnableVertexAttribArray(2);

	glGenVertexArrays(1, &VAO2);
	glGenBuffers(1, &VBO2);
	glGenBuffers(1, &EBO2);
	glBindVertexArray(VAO2);
	glBindBuffer(GL_ARRAY_BUFFER, VBO2);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesMoon), verticesMoon, GL_STATIC_DRAW);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO2);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	// pozisyon baþlangýcý
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	// renk baþlangýcý
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);
	// doku koordinatý baþlangýcý
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
	glEnableVertexAttribArray(2);

	glGenVertexArrays(1, &VAO3);
	glGenBuffers(1, &VBO3);
	glGenBuffers(1, &EBO3);
	glBindVertexArray(VAO3);
	glBindBuffer(GL_ARRAY_BUFFER, VBO3);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesMan), verticesMan, GL_STATIC_DRAW);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO3);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	// pozisyon baþlangýcý
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	// renk baþlangýcý
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);
	// doku koordinatý baþlangýcý
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
	glEnableVertexAttribArray(2);

	glGenVertexArrays(1, &VAO4);
	glGenBuffers(1, &VBO4);
	glGenBuffers(1, &EBO4);
	glBindVertexArray(VAO4);
	glBindBuffer(GL_ARRAY_BUFFER, VBO4);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesGrass), verticesGrass, GL_STATIC_DRAW);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO4);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	// pozisyon baþlangýcý
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	// renk baþlangýcý
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);
	// doku koordinatý baþlangýcý
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
	glEnableVertexAttribArray(2);

	glGenVertexArrays(1, &VAO5);
	glGenBuffers(1, &VBO5);
	glGenBuffers(1, &EBO5);
	glBindVertexArray(VAO5);
	glBindBuffer(GL_ARRAY_BUFFER, VBO5);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesCat), verticesCat, GL_STATIC_DRAW);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO5);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	// pozisyon baþlangýcý
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	// renk baþlangýcý
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);
	// doku koordinatý baþlangýcý
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
	glEnableVertexAttribArray(2);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

	// Texturelar oluþturulur, aktive edilir ve baðlanýr
	// uygun texture birimlerine uygun texturelar yüklenir
	GLuint texture1, texture2, texture3,
		   texture4, texture5, texture6;

	glGenTextures(1, &texture1);
	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, texture1);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);	
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	int widthImage, heightImage, numColCh;
	stbi_set_flip_vertically_on_load(true);
	unsigned char* data = stbi_load("mountain.png", &widthImage, &heightImage, &numColCh, 0);
	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImage, heightImage, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
	stbi_image_free(data);
	glBindTexture(GL_TEXTURE_2D, 0);
	
	glGenTextures(1, &texture2);
	glActiveTexture(GL_TEXTURE1);
	glBindTexture(GL_TEXTURE_2D, texture2);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	stbi_set_flip_vertically_on_load(true);
	data = stbi_load("moon.png", &widthImage, &heightImage, &numColCh, 0);
	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImage, heightImage, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
	stbi_image_free(data);
	glBindTexture(GL_TEXTURE_2D, 0);

	glGenTextures(1, &texture3);
	glActiveTexture(GL_TEXTURE2);
	glBindTexture(GL_TEXTURE_2D, texture3);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	stbi_set_flip_vertically_on_load(true);
	data = stbi_load("man.png", &widthImage, &heightImage, &numColCh, 0);
	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImage, heightImage, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
	stbi_image_free(data);
	glBindTexture(GL_TEXTURE_2D, 0);

	glGenTextures(1, &texture4);
	glActiveTexture(GL_TEXTURE3);
	glBindTexture(GL_TEXTURE_2D, texture4);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	stbi_set_flip_vertically_on_load(true);
	data = stbi_load("grass.png", &widthImage, &heightImage, &numColCh, 0);
	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImage, heightImage, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
	stbi_image_free(data);
	glBindTexture(GL_TEXTURE_2D, 0);

	glGenTextures(1, &texture5);
	glActiveTexture(GL_TEXTURE4);
	glBindTexture(GL_TEXTURE_2D, texture5);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	stbi_set_flip_vertically_on_load(true);
	data = stbi_load("cat.png", &widthImage, &heightImage, &numColCh, 0);
	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, widthImage, heightImage, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
	stbi_image_free(data);
	glBindTexture(GL_TEXTURE_2D, 0);

	// freetype init edilir ve font yüklenir
	FT_Library ft;
	if (FT_Init_FreeType(&ft))
	{
		std::cout << "Could not init Freetype library" << std::endl;
		return -1;
	}
	
	std::string fontName = FileSystem::getPath("Antonio-Bold.ttf");
	if(fontName.empty())
	{
		std::cout << "Failed to load fontName" << std::endl;
		return -1;
	}

	FT_Face face;
	if (FT_New_Face(ft, fontName.c_str(), 0, &face))
	{
		std::cout << "Failed to load font: " << fontName << std::endl;
		FT_Error error = FT_New_Face(ft, fontName.c_str(), 0, &face);
		if (error != 0)
		{
			std::cout << "FreeType error code: " << error << std::endl;
		}
		return -1;
	}
	else
	{
		// init ve font yükleme iþlemlerinden sonra
		// her karakterin glyph'i yüklenir ve saklanýr
		FT_Set_Pixel_Sizes(face, 0, 48);
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
		for (unsigned char c = 0; c < 128; c++)
		{
			if (FT_Load_Char(face, c, FT_LOAD_RENDER))
			{
				std::cout << "Failed to load glyph" << std::endl;
				continue;
			}

			glGenTextures(1, &texture6);
			glBindTexture(GL_TEXTURE_2D, texture6);

			glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, face->glyph->bitmap.width, face->glyph->bitmap.rows,
				0, GL_RED, GL_UNSIGNED_BYTE, face->glyph->bitmap.buffer);

			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

			Character character
			{
				texture6,
				glm::ivec2(face->glyph->bitmap.width, face->glyph->bitmap.rows),
				glm::ivec2(face->glyph->bitmap_left, face->glyph->bitmap_top),
				static_cast<unsigned int>(face->glyph->advance.x)
			};
			Characters.insert(std::pair<char, Character>(c, character));
		}
		glBindTexture(GL_TEXTURE_2D, 0);
	}
	FT_Done_Face(face);
	FT_Done_FreeType(ft);

	// text renderlama için bufferlar baðlanýr
	glGenVertexArrays(1, &textVAO);
	glGenBuffers(1, &textVBO);
	glBindVertexArray(textVAO);
	glBindBuffer(GL_ARRAY_BUFFER, textVBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(float) * 6 * 4, NULL, GL_DYNAMIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * sizeof(float), 0);
	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

	// shader programý çalýþtýrýlýr, ardýndan her texture bir indeks alarak
	// sahnede ayný anda bulunur
	shaderProgram.use();

	glUniform1i(glGetUniformLocation(shaderProgram.ID, "texture1"), 0);
	glUniform1i(glGetUniformLocation(shaderProgram.ID, "texture2"), 1);
	glUniform1i(glGetUniformLocation(shaderProgram.ID, "texture3"), 2);
	glUniform1i(glGetUniformLocation(shaderProgram.ID, "texture4"), 3);
	glUniform1i(glGetUniformLocation(shaderProgram.ID, "texture5"), 4);
	glUniform1i(glGetUniformLocation(shaderProgram.ID, "texture6"), 5);

	// arkaplan rengi atanýr
	glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT);
	glfwSwapBuffers(window);

	glEnable(GL_DEPTH_TEST);

	while(!glfwWindowShouldClose(window))
	{
		glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		// sahnede objelerin ve texturelarýn daha iyi gözükmesi için
		// glm kütüphanesi kullanýlýr
		glm::mat4 model = glm::mat4(1.0f);
		glm::mat4 view = glm::mat4(1.0f);
		glm::mat4 projScene = glm::mat4(1.0f);
		view = glm::translate(view, glm::vec3(0.0f, -0.15f, -1.1f)); // cisimlerin uzaklýðý ayarlanýr
		projScene = glm::perspective(glm::radians(45.0f), (float)(width / height), 0.1f, 100.0f);

		int modelLoc = glGetUniformLocation(shaderProgram.ID, "model");
		glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
		int viewLoc = glGetUniformLocation(shaderProgram.ID, "view");
		glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));
		int projSceneLoc = glGetUniformLocation(shaderProgram.ID, "projection");
		glUniformMatrix4fv(projSceneLoc, 1, GL_FALSE, glm::value_ptr(projScene));

		shaderProgram.use();

		// her buffer ve her texture sýrayla tekrar baðlanýr ve çizdirilir
		glBindTexture(GL_TEXTURE_2D, texture1);
		glBindVertexArray(VAO1);
		glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), GL_UNSIGNED_INT, 0);

		glBindTexture(GL_TEXTURE_2D, texture2);
		glBindVertexArray(VAO2);
		glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), GL_UNSIGNED_INT, 0);

		glBindTexture(GL_TEXTURE_2D, texture3);
		glBindVertexArray(VAO3);
		glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), GL_UNSIGNED_INT, 0);

		glBindTexture(GL_TEXTURE_2D, texture4);
		glBindVertexArray(VAO4);
		glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), GL_UNSIGNED_INT, 0);

		glBindTexture(GL_TEXTURE_2D, texture5);
		glBindVertexArray(VAO5);
		glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(int), GL_UNSIGNED_INT, 0);
		
		// text renderlama fomksiyonu
		// maalesef baþarýsýz
		RenderText(shaderText, "Return to Nature", verticesText[0], verticesText[1], 0.5f, glm::vec3(0.0f, 1.0f, 0.0f));

		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	// program sonunda bufferlar serbest býrakýlýr
	glDeleteVertexArrays(1, &VAO1);
	glDeleteBuffers(1, &VBO1);
	glDeleteBuffers(1, &EBO1);
	glDeleteVertexArrays(1, &VAO2);
	glDeleteBuffers(1, &VBO2);
	glDeleteBuffers(1, &EBO2);
	glDeleteVertexArrays(1, &VAO3);
	glDeleteBuffers(1, &VBO3);
	glDeleteBuffers(1, &EBO3);
	glDeleteVertexArrays(1, &VAO4);
	glDeleteBuffers(1, &VBO4);
	glDeleteBuffers(1, &EBO4);
	glDeleteVertexArrays(1, &VAO5);
	glDeleteBuffers(1, &VBO5);
	glDeleteBuffers(1, &EBO5);
	glDeleteVertexArrays(1, &textVAO);
	glDeleteBuffers(1, &textVBO);
	glDeleteTextures(1, &texture1);
	glDeleteTextures(1, &texture2);
	glDeleteTextures(1, &texture3);
	glDeleteTextures(1, &texture4);
	glDeleteTextures(1, &texture5);
	glDeleteTextures(1, &texture6);
	glDisable(GL_BLEND);

	// pencere kapanýr ve program sonlanýr
	glfwDestroyWindow(window);
	glfwTerminate();
	return 0;
}

// text renderlama fonksiyonu
void RenderText(Shader& shader, std::string text, float x, float y, float scale, glm::vec3 color)
{
	shader.use();
	glUniform3f(glGetUniformLocation(shader.ID, "textColor"), color.x, color.y, color.z);
	glActiveTexture(GL_TEXTURE5);
	glBindVertexArray(textVAO);

	// stringdeki karakterler sýrayla itere edilir
	std::string::const_iterator c;
	for (c = text.begin(); c != text.end(); c++)
	{
		Character ch = Characters[*c];

		float xpos = x + ch.Bearing.x * scale;
		float ypos = y - (ch.Size.y - ch.Bearing.y) * scale;

		float w = ch.Size.x * scale;
		float h = ch.Size.y * scale;
		// her karakter için VBO güncellenir
		float vertices[6][4] = {
			{ xpos,     ypos + h,   0.0f, 0.0f },
			{ xpos,     ypos,       0.0f, 1.0f },
			{ xpos + w, ypos,       1.0f, 1.0f },

			{ xpos,     ypos + h,   0.0f, 0.0f },
			{ xpos + w, ypos,       1.0f, 1.0f },
			{ xpos + w, ypos + h,   1.0f, 0.0f }
		};
		// obje üstüne glyph texture'ý baðlanýr
		glBindTexture(GL_TEXTURE_2D, ch.TextureID);
		// VBO belleðinin içeriði güncellenir
		glBindBuffer(GL_ARRAY_BUFFER, textVBO);
		glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(vertices), vertices); 

		glBindBuffer(GL_ARRAY_BUFFER, 0);
		// obje çizdirilir
		glDrawArrays(GL_TRIANGLES, 0, 6);
		// imleç bir saða kaydýrýlýr
		x += (ch.Advance >> 6) * scale;
	}
	glBindVertexArray(0);
	glBindTexture(GL_TEXTURE_2D, 0);
}
