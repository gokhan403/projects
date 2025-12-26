#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <stb_image.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <learnopengl/filesystem.h>
#include <learnopengl/shader.h>
#include <learnopengl/camera.h>
#include <learnopengl/model.h>

#include <iostream>
#include <cmath>
#include <Windows.h>

void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void mouse_callback(GLFWwindow* window, double xpos, double ypos);
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
void processInput(GLFWwindow* window);
void noktaCiz(glm::vec4 bezierEgriNoktasi);
void binomyalKatsayilar(GLint n, GLint* C);
void bezierNoktasiHesapla(GLfloat u, glm::vec4* bezierNoktasi, GLint kontrolNoktasiSayisi, glm::vec4* kontrolNoktalari, GLint* C);
void bezier(GLint kontrolNoktasiSayisi, glm::vec4* kontrolNoktalari, GLint BezierEgrisiNoktaSayisi);

// ekran boyutlarý
const unsigned int width = 800;
const unsigned int height = 600;

// kamera
Camera camera(glm::vec3(0.0f, 0.0f, 100.0f));
float lastX = (float)width / 2.0;
float lastY = (float)height / 2.0;
bool firstMouse = true;

// zamanlayýcýlar
float deltaTime = 0.0f;
float lastFrame = 0.0f;

int main()
{
	// konfigürasyon
	glfwInit();
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	// pencere oluþturulur
	GLFWwindow* window = glfwCreateWindow(width, height, "OpenGL Lab6", NULL, NULL);
	if(window == NULL)
	{
		std::cout << "Failed to create GLFW window" << std::endl;

		glfwTerminate();
		return -1;
	}
	//pencere fonksiyonlarý 
	glfwMakeContextCurrent(window);
	glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
	//mouse fonksiyonlarý
	glfwSetCursorPosCallback(window, mouse_callback);
	glfwSetScrollCallback(window, scroll_callback);

	// mouse inputu
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

	// OpenGL fonksiyonlarý yüklenir
	gladLoadGL();
	glEnable(GL_DEPTH_TEST);

	// shaderlar oluþturulur ve model yüklenir
	Shader shader("default.vert", "default.frag");
	Shader shaderLines("new.vert", "new.frag");

	Model helecopter(FileSystem::getPath("models/helecopter/chopper.obj"));

	// kooridnat siteminin x ekseni çizdirmek için koordinatlar
	float verticesX[] = 
	{
		 0.0f, 0.0f, 0.0f,
		 1.0f, 0.0f, 0.0f,
		 2.0f, 0.0f, 0.0f,
		 3.0f, 0.0f, 0.0f,
		 4.0f, 0.0f, 0.0f,
		 5.0f, 0.0f, 0.0f,
		 6.0f, 0.0f, 0.0f,
		 7.0f, 0.0f, 0.0f,
		 8.0f, 0.0f, 0.0f,
		 9.0f, 0.0f, 0.0f,
		 10.0f, 0.0f, 0.0f,
		 11.0f, 0.0f, 0.0f,
		 12.0f, 0.0f, 0.0f,
		 13.0f, 0.0f, 0.0f,
		 14.0f, 0.0f, 0.0f,
		 15.0f, 0.0f, 0.0f,
		 16.0f, 0.0f, 0.0f,
		 17.0f, 0.0f, 0.0f,
		 18.0f, 0.0f, 0.0f,
		 19.0f, 0.0f, 0.0f,
		 20.0f, 0.0f, 0.0f,
		 21.0f, 0.0f, 0.0f,
		 22.0f, 0.0f, 0.0f,
		 23.0f, 0.0f, 0.0f,
		 24.0f, 0.0f, 0.0f,
		 25.0f, 0.0f, 0.0f,
		 26.0f, 0.0f, 0.0f,
		 27.0f, 0.0f, 0.0f,
		 28.0f, 0.0f, 0.0f,
		 29.0f, 0.0f, 0.0f,
		 30.0f, 0.0f, 0.0f,
		 31.0f, 0.0f, 0.0f,
		 32.0f, 0.0f, 0.0f,
		 33.0f, 0.0f, 0.0f,
		 34.0f, 0.0f, 0.0f,
		 35.0f, 0.0f, 0.0f,
		 36.0f, 0.0f, 0.0f,
		 37.0f, 0.0f, 0.0f,
		 38.0f, 0.0f, 0.0f,
		 39.0f, 0.0f, 0.0f,
		 40.0f, 0.0f, 0.0f,
		 41.0f, 0.0f, 0.0f,
		 42.0f, 0.0f, 0.0f,
		 43.0f, 0.0f, 0.0f,
		 44.0f, 0.0f, 0.0f,
		 45.0f, 0.0f, 0.0f,
		 46.0f, 0.0f, 0.0f,
		 47.0f, 0.0f, 0.0f,
		 48.0f, 0.0f, 0.0f,
		 49.0f, 0.0f, 0.0f,
		 50.0f, 0.0f, 0.0f
	};

	// kooridnat siteminin y ekseni çizdirmek için koordinatlar
	float verticesY[] = 
	{ 
		0.0f, 0.0f, 0.0f,	
		0.0f, 1.0f, 0.0f,	
		0.0f, 2.0f, 0.0f,	
		0.0f, 3.0f, 0.0f,
		0.0f, 4.0f, 0.0f,	
		0.0f, 5.0f, 0.0f,	
		0.0f, 6.0f, 0.0f,	
		0.0f, 7.0f, 0.0f,	
		0.0f, 8.0f, 0.0f,	
		0.0f, 9.0f, 0.0f,
		0.0f, 10.0f, 0.0f,
		0.0f, 11.0f, 0.0f,
		0.0f, 12.0f, 0.0f,
		0.0f, 13.0f, 0.0f,
		0.0f, 14.0f, 0.0f,
		0.0f, 15.0f, 0.0f,
		0.0f, 16.0f, 0.0f,
		0.0f, 17.0f, 0.0f,
		0.0f, 18.0f, 0.0f,
		0.0f, 19.0f, 0.0f,
		0.0f, 20.0f, 0.0f,
		0.0f, 21.0f, 0.0f,
		0.0f, 22.0f, 0.0f,
		0.0f, 23.0f, 0.0f,
		0.0f, 24.0f, 0.0f,
		0.0f, 25.0f, 0.0f,
		0.0f, 26.0f, 0.0f,
		0.0f, 27.0f, 0.0f,
		0.0f, 28.0f, 0.0f,
		0.0f, 29.0f, 0.0f,
		0.0f, 30.0f, 0.0f,
		0.0f, 31.0f, 0.0f,
		0.0f, 32.0f, 0.0f,
		0.0f, 33.0f, 0.0f,
		0.0f, 34.0f, 0.0f,
		0.0f, 35.0f, 0.0f,
		0.0f, 36.0f, 0.0f,
		0.0f, 37.0f, 0.0f,
		0.0f, 38.0f, 0.0f,
		0.0f, 39.0f, 0.0f,
		0.0f, 40.0f, 0.0f,
		0.0f, 41.0f, 0.0f,
		0.0f, 42.0f, 0.0f,
		0.0f, 43.0f, 0.0f,
		0.0f, 44.0f, 0.0f,
		0.0f, 45.0f, 0.0f,
		0.0f, 46.0f, 0.0f,
		0.0f, 47.0f, 0.0f,
		0.0f, 48.0f, 0.0f,
		0.0f, 49.0f, 0.0f,
		0.0f, 50.0f, 0.0f
	};

	// kooridnat siteminin z ekseni çizdirmek için koordinatlar
	float verticesZ[] = 
	{ 
		0.0f, 0.0f, 0.0f,	
		0.0f, 0.0f, 1.0f,	
		0.0f, 0.0f, 2.0f,	
		0.0f, 0.0f, 3.0f,	
		0.0f, 0.0f, 4.0f,	
		0.0f, 0.0f, 5.0f,	
		0.0f, 0.0f, 6.0f,	
		0.0f, 0.0f, 7.0f,	
		0.0f, 0.0f, 8.0f,
		0.0f, 0.0f, 9.0f,	
		0.0f, 0.0f, 10.0f,
		0.0f, 0.0f, 11.0f,
		0.0f, 0.0f, 12.0f,
		0.0f, 0.0f, 13.0f,
		0.0f, 0.0f, 14.0f,
		0.0f, 0.0f, 15.0f,
		0.0f, 0.0f, 16.0f,
		0.0f, 0.0f, 17.0f,
		0.0f, 0.0f, 18.0f,
		0.0f, 0.0f, 19.0f,
		0.0f, 0.0f, 20.0f,
		0.0f, 0.0f, 21.0f,
		0.0f, 0.0f, 22.0f,
		0.0f, 0.0f, 23.0f,
		0.0f, 0.0f, 24.0f,
		0.0f, 0.0f, 25.0f,
		0.0f, 0.0f, 26.0f,
		0.0f, 0.0f, 27.0f,
		0.0f, 0.0f, 28.0f,
		0.0f, 0.0f, 29.0f,
		0.0f, 0.0f, 30.0f,
		0.0f, 0.0f, 31.0f,
		0.0f, 0.0f, 32.0f,
		0.0f, 0.0f, 33.0f,
		0.0f, 0.0f, 34.0f,
		0.0f, 0.0f, 35.0f,
		0.0f, 0.0f, 36.0f,
		0.0f, 0.0f, 37.0f,
		0.0f, 0.0f, 38.0f,
		0.0f, 0.0f, 39.0f,
		0.0f, 0.0f, 40.0f,
		0.0f, 0.0f, 41.0f,
		0.0f, 0.0f, 42.0f,
		0.0f, 0.0f, 43.0f,
		0.0f, 0.0f, 44.0f,
		0.0f, 0.0f, 45.0f,
		0.0f, 0.0f, 46.0f,
		0.0f, 0.0f, 47.0f,
		0.0f, 0.0f, 48.0f,
		0.0f, 0.0f, 49.0f,
		0.0f, 0.0f, 50.0f
	};

	// þerit için kontrol noktalarý
	glm::vec4 controlPoints[5] = 
	{   {5.0, 5.0, 5.0, 1.0},
		{5.0, -8.0, -10.0, 1.0},  
		{-7.0, 8.0, -15.0, 1.0},
		{-4.0, -4.0, 10.0, 1.0}, 
		{5.0, 5.0, 5.0, 1.0} 
	};


	//VAO ve VBO'lar oluþturulup atanýr
	unsigned int VAO1, VBO1, VAO2, VBO2, VAO3, VBO3, VAO4, VBO4;

	glGenVertexArrays(1, &VAO1);
	glGenBuffers(1, &VBO1);
	glBindVertexArray(VAO1);
	glBindBuffer(GL_ARRAY_BUFFER, VBO1);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesX), verticesX, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);

	glGenVertexArrays(1, &VAO2);
	glGenBuffers(1, &VBO2);
	glBindVertexArray(VAO2);
	glBindBuffer(GL_ARRAY_BUFFER, VBO2);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesY), verticesY, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);

	glGenVertexArrays(1, &VAO3);
	glGenBuffers(1, &VBO3);
	glBindVertexArray(VAO3);
	glBindBuffer(GL_ARRAY_BUFFER, VBO3);
	glBufferData(GL_ARRAY_BUFFER, sizeof(verticesZ), verticesZ, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);

	glGenVertexArrays(1, &VAO4);
	glGenBuffers(1, &VBO4);
	glBindVertexArray(VAO4);
	glBindBuffer(GL_ARRAY_BUFFER, VBO4);
	glBufferData(GL_ARRAY_BUFFER, sizeof(controlPoints), controlPoints, GL_STATIC_DRAW);
	glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

	// helikopter animasyonu için kullanýlacak bazý deðerler
	float rotateVal = 3.0f;
	GLfloat u;
	GLint k = 0;
	while(!glfwWindowShouldClose(window))
	{
		// 60 hz için 17 ms uyutma
		//Sleep(17);
		
		//frame baþý zaman mantýðý
		float currentFrame = static_cast<float>(glfwGetTime());
		deltaTime = currentFrame - lastFrame;
		lastFrame = currentFrame;

		// helikopter þeridin son noktasýna ulaþtýðýnda
		// baþlangýç noktasýna atanýr
		if (k >= 5000)
			k = 0;

		// klavye ve fare girdileri ekrana verilir
		processInput(window);

		glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		//dönüþüm matrisleri konfigürasyonu
		glm::mat4 projection = glm::perspective(glm::radians(45.0f), (float)width / (float)height, 0.1f, 1000.0f);
		glm::mat4 view = camera.GetViewMatrix();
		shader.use();
		shader.setMat4("projection", projection);
		shader.setMat4("view", view);
		shaderLines.use();
		shaderLines.setMat4("projection", projection);
		shaderLines.setMat4("view", view);

		//modeller ve renkler atanýp VAO'lar baðlanarak
		//koordinat eksenleri çizilir
		glm::mat4 modelX = glm::mat4(1.0f);
		shaderLines.setMat4("model", modelX);
		shaderLines.setVec3("lineColor", glm::vec3(1.0f, 0.0f, 0.0f));
		glBindVertexArray(VAO1);
		glDrawArrays(GL_LINES, 0, 51);

		glm::mat4 modelY = glm::mat4(1.0f);
		shaderLines.setMat4("model", modelY);
		shaderLines.setVec3("lineColor", glm::vec3(0.0f, 1.0f, 0.0f));
		glBindVertexArray(VAO2);
		glDrawArrays(GL_LINES, 0, 51);

		glm::mat4 modelZ = glm::mat4(1.0f);
		shaderLines.setMat4("model", modelZ);
		shaderLines.setVec3("lineColor", glm::vec3(0.0f, 0.0f, 1.0f));
		glBindVertexArray(VAO3);
		glDrawArrays(GL_LINES, 0, 51);

		// þerit çizdirilir
		glm::mat4 modelSpline = glm::mat4(1.0f);
		modelSpline = glm::scale(modelSpline, glm::vec3(5.0f, 5.0f, 5.0f));
		shaderLines.setMat4("model", modelSpline);
		shaderLines.setVec3("lineColor", glm::vec3(0.0f, 0.5f, 0.5f));
		glBindVertexArray(VAO4);
		bezier(5, controlPoints, 5000);

		// helikoter çizimi için doku atanýr
		shader.use();
		shader.setInt("texture_diffuse1", 0);

		// helikopterin animasyonu için þerit üzerindeki noktalar
		// her frame'de birer birer oluþturulup tutulur
		GLint* C;
		C = new GLint[5];
		binomyalKatsayilar(4, C);
		u = GLfloat(k) / GLfloat(5000);
		glm::vec4 next;
		bezierNoktasiHesapla(u, &next, 5, controlPoints, C);

		// helikopter uygun koordinatlar ve döndürme açýlarý ile
		// her frame'de uygun pozisyona çizdirilerek animasyon gerçekleþir
		glm::mat4 modelHelecopter = glm::mat4(1.0f);
		modelHelecopter = glm::translate(modelHelecopter, glm::vec3(5 * next.x, 5 * next.y, 5 * next.z));
		modelHelecopter = glm::rotate(modelHelecopter, glm::radians(rotateVal), glm::vec3(0.0f, 1.0f, 0.0f));
		shader.setMat4("model", modelHelecopter);
		helecopter.Draw(shader);

		// sonraki nokta deðeri için k 1 artýrýlýr ve
		// her noktada uygun döndürme deðeri için rotateVal artýrýlýr
		k += 1;
		rotateVal += 360.0f / 5000.0f;

		// görüntüyü iþleme fonksiyonlarý
		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	// program sonlandýrýlýr
	glfwTerminate();
	return 0;
}

// mouse, klavye ve pencere fonksiyonlarý
void processInput(GLFWwindow* window)
{
	if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
		glfwSetWindowShouldClose(window, true);

	if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
		camera.ProcessKeyboard(FORWARD, deltaTime);
	if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
		camera.ProcessKeyboard(BACKWARD, deltaTime);
	if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
		camera.ProcessKeyboard(LEFT, deltaTime);
	if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
		camera.ProcessKeyboard(RIGHT, deltaTime);
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
	glViewport(0, 0, width, height);
}

void mouse_callback(GLFWwindow* window, double xposIn, double yposIn)
{
	float xpos = static_cast<float>(xposIn);
	float ypos = static_cast<float>(yposIn);

	if(firstMouse)
	{
		lastX = xpos;
		lastY = ypos;
		firstMouse = false;
	}

	float xoffset = xpos - lastX;
	float yoffset = lastY - ypos;

	lastX = xpos;
	lastY = ypos;

	camera.ProcessMouseMovement(xoffset, yoffset);
}

void scroll_callback(GLFWwindow* window, double xoffset, double yoffset)
{
	camera.ProcessMouseScroll(static_cast<float>(yoffset));
}

// bezier þeridini çizdirmek için kullanýlan fonksiyonlar
void noktaCiz(glm::vec4 bezierEgriNoktasi) 
{
	glBegin(GL_POINTS);
	glVertex3f(bezierEgriNoktasi.x, bezierEgriNoktasi.y, bezierEgriNoktasi.z);
	glEnd();
}

/* Verilen n deðerine göre C binomyal katsayýlarýný hesaplar. */
void binomyalKatsayilar(GLint n, GLint* C) 
{
	GLint k, j;

	for (k = 0; k <= n; k++) {
		/* n!/(k!*(n-k)!) hesabý */
		C[k] = 1;
		for (j = n; j >= k + 1; j--)
			C[k] *= j;
		for (j = n - k; j >= 2; j--)
			C[k] /= j;
	}
}

void bezierNoktasiHesapla(GLfloat u, glm::vec4* bezierNoktasi, GLint kontrolNoktasiSayisi, glm::vec4* kontrolNoktalari, GLint* C) 
{
	GLint k, n = kontrolNoktasiSayisi - 1;
	GLfloat bezierTabanFonksiyonu;
	bezierNoktasi->x = bezierNoktasi->y = bezierNoktasi->z = 0.0;
	/* Taban fonksiyonlarýný hesapla ve kontrol noktalarýný harmanla */
	for (k = 0; k < kontrolNoktasiSayisi; k++) {
		bezierTabanFonksiyonu = C[k] * (GLfloat)pow(u, k) * (GLfloat)pow(1 - u, n - k);
		bezierNoktasi->x += kontrolNoktalari[k].x * bezierTabanFonksiyonu;
		bezierNoktasi->y += kontrolNoktalari[k].y * bezierTabanFonksiyonu;
		bezierNoktasi->z += kontrolNoktalari[k].z * bezierTabanFonksiyonu;
	}
}

void bezier(GLint kontrolNoktasiSayisi, glm::vec4* kontrolNoktalari, GLint BezierEgrisiNoktaSayisi) 
{
	glm::vec4 bezierEgrisiNoktasi;
	GLfloat u;
	GLint* C, k;
	/* Binomyal katsayýlar iiçin alan ayýr. */
	C = new GLint[kontrolNoktasiSayisi];
	binomyalKatsayilar(kontrolNoktasiSayisi - 1, C);

	for (k = 0; k <= BezierEgrisiNoktaSayisi; k++) {
		u = GLfloat(k) / GLfloat(BezierEgrisiNoktaSayisi);
		bezierNoktasiHesapla(u, &bezierEgrisiNoktasi, kontrolNoktasiSayisi, kontrolNoktalari, C);
		noktaCiz(bezierEgrisiNoktasi);
	}
	delete[] C;
}
