#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <iostream>

const char* vertexShaderSource = "#version 330 core\n"
"layout (location = 0) in vec3 aPos;\n"
"layout (location = 1) in vec3 aColor;\n"
"out vec3 ourColor;\n"
"uniform mat4 model;\n"
"uniform mat4 view;\n"
"uniform mat4 projection;\n"
"void main()\n"
"{\n"
"   gl_Position = projection * view * model * vec4(aPos, 1.0);\n"
"   ourColor = aColor;\n"
"}\0";

const char* fragmentShaderSource = "#version 330 core\n"
"out vec4 FragColor;\n"
"in vec3 ourColor;\n"
"void main()\n"
"{\n"
"   FragColor = vec4(ourColor, 0.3f);\n"
"}\n\0";

// pencere boyutları
const unsigned int width = 800;
const unsigned int height = 600;

int main()
{
	// opengl aktifleştirilir ve versiyon belirlenir
	glfwInit();

	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	// kübün koordinatları ve renkleri
	GLfloat vertices[] =
	{
		// koordinatlar		 // renkler	
		-0.5f, 0.0f,  0.5f,  1.0f, 0.0f, 0.0f,	
		-0.5f, 0.0f, -0.5f,  1.0f, 1.0f, 0.0f, 
		 0.5f, 0.0f, -0.5f,	 1.0f, 0.0f, 1.0f, 
		 0.5f, 0.0f,  0.5f,	 0.0f, 1.0f, 0.0f, 
		-0.5f, 1.0f,  0.5f,	 0.0f, 1.0f, 1.0f, 
		-0.5f, 1.0f, -0.5f,	 0.0f, 0.0f, 1.0f, 
		 0.5f, 1.0f, -0.5f,	 0.5f, 0.0f, 0.5f, 
		 0.5f, 1.0f,  0.5f,  0.0f, 0.5f, 0.5f
	};
	
	// üçgenlerin çizileceği sıra için koordinatların indeksleri
	GLuint indices[] =
	{
		0, 1, 2,
		0, 2, 3,
		0, 4, 5,
		0, 5, 1,
		1, 5, 6,
		1, 6, 2,
		2, 6, 7,
		2, 7, 3,
		0, 4, 7,
		0, 7, 3,
		4, 5, 6,
		4, 6, 7
	};
	
	// opengl penceresi oluşturulur
	GLFWwindow* window = glfwCreateWindow(width, height, "OpenGL Lab2", NULL, NULL);
	if(window == NULL)
	{
		std::cout << "Failed to create GLFW window!" << std::endl;

		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);

	// opengl fonksiyonları yüklenir ve 
	//koordinat sisteminin pencerede nereden başlayacağı atanır
	gladLoadGL();
	glViewport(0, 0, width, height);

	// vertex shader oluşturulur
	GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
	glCompileShader(vertexShader);

	// fragment shader oluşturulur
	GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);

	// shader programı oluşturulur ve bağlanır
	GLuint shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, vertexShader);
	glAttachShader(shaderProgram, fragmentShader);
	glLinkProgram(shaderProgram);

	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

	// bufferlar oluşturulur ve bağlanır
	GLuint VAO, VBO, EBO;

	glGenVertexArrays(1, &VAO);
	glGenBuffers(1, &VBO);
	glGenBuffers(1, &EBO);
	glBindVertexArray(VAO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

	// arkaplan rengi atanır
	glClearColor(0.2f, 0.2f, 0.2f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT);
	glfwSwapBuffers(window);

	glEnable(GL_DEPTH_TEST);

	// kübün rotasyonu için bazı değerler
	float rotation = 0.0f;
	double prevTime = glfwGetTime();

	// renk harmanlama aktifleştirilir
	glEnable(GL_BLEND);
	while(!glfwWindowShouldClose(window))
	{
		// pencere açık olduğu sürece arkaplan rengi,
		// shader programı ve VAO aktif tutulur
		glClearColor(0.2f, 0.2f, 0.2f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glUseProgram(shaderProgram);
		glBindVertexArray(VAO);

		// kübün rotasyonu sağlanır
		double crntTime = glfwGetTime();
		if(crntTime - prevTime >= 1 / 60)
		{
			rotation += 0.01f;
			prevTime = crntTime;
		}

		// üç boyuta geçiş
		glm::mat4 model = glm::mat4(1.0f);
		glm::mat4 view = glm::mat4(1.0f);
		glm::mat4 proj = glm::mat4(1.0f);
		model = glm::rotate(model, glm::radians(rotation), glm::vec3(1.0f, 1.0f, 1.0f));
		view = glm::translate(view, glm::vec3(0.0f, 0.0f, -5.0f));
		proj = glm::perspective(glm::radians(45.0f), (float)(width / height), 0.1f, 100.0f);

		int modelLoc = glGetUniformLocation(shaderProgram, "model");
		glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
		int viewLoc = glGetUniformLocation(shaderProgram, "view");
		glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));
		int projLoc = glGetUniformLocation(shaderProgram, "projection");
		glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm::value_ptr(proj));
		
		// renk harmanlama
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		// küp çizdirilir
		glShadeModel(GL_SMOOTH);
		glDrawElements(GL_TRIANGLES, sizeof(indices)/sizeof(int), GL_UNSIGNED_INT, 0);
		glfwSwapBuffers(window);

		glfwPollEvents();
	}

	// program sonunda bufferlar boşa çıkarılır
	glDeleteVertexArrays(1, &VAO);
	glDeleteBuffers(1, &VBO);
	glDeleteBuffers(1, &EBO);
	glDeleteProgram(shaderProgram);
	glDisable(GL_BLEND);

	// pencere kapanır ve program sonlanır
	glfwDestroyWindow(window);
	glfwTerminate();
	return 0;
}
