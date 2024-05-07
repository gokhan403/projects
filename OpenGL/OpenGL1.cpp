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

void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void mouse_callback(GLFWwindow* window, double xpos, double ypos);
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
void processInput(GLFWwindow* window);

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
	GLFWwindow* window = glfwCreateWindow(width, height, "OpenGL Lab5", NULL, NULL);
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
	//ve durum belirtilir
	gladLoadGL();
	glEnable(GL_DEPTH_TEST);

	// shader oluþturulur ve modeller yüklenir
	Shader shader("default.vert", "default.frag");
	Shader shaderLines("new.vert", "new.frag");

	Model teapot1(FileSystem::getPath("models/teapot/teapot.obj"));
	Model teapot2(FileSystem::getPath("models/teapot/teapot.obj"));
	Model teapot3(FileSystem::getPath("models/teapot/teapot.obj"));
	Model teapot4(FileSystem::getPath("models/teapot/teapot.obj"));
	Model planet1(FileSystem::getPath("models/planet/planet.obj"));
	Model planet2(FileSystem::getPath("models/planet/planet.obj"));
	Model rock(FileSystem::getPath("models/rock/rock.obj"));
	
	// çaydanlýk modelleri için texturelar yüklenir
	unsigned int texture1 = TextureFromFile("green.png", FileSystem::getPath("models/teapot"));
	unsigned int texture2 = TextureFromFile("top.png", FileSystem::getPath("models/teapot"));
	unsigned int texture3 = TextureFromFile("wood_dark.png", FileSystem::getPath("models/teapot"));
	unsigned int texture4 = TextureFromFile("spots.png", FileSystem::getPath("models/teapot"));

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

	//VAO ve VBO'lar oluþturulup atanýr
	unsigned int VAO1, VBO1, VAO2, VBO2, VAO3, VBO3;

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

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

	while(!glfwWindowShouldClose(window))
	{
		//frame baþý zaman mantýðý
		float currentFrame = static_cast<float>(glfwGetTime());
		deltaTime = currentFrame - lastFrame;
		lastFrame = currentFrame;

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

		shader.use();
		shader.setInt("texture_diffuse1", 0);

		//1. dönüþüm yapýlarak yeþil çaydanlýk çizdirilir
		glBindTexture(GL_TEXTURE_2D, texture1);
		glm::mat4 modelTeapot1= glm::mat4(1.0f);
		modelTeapot1 = glm::translate(modelTeapot1, glm::vec3(-10.0f, -10.0f, -10.0f));
		modelTeapot1 = glm::scale(modelTeapot1, glm::vec3(0.5f, 0.5f, 0.5f));
		shader.setMat4("model", modelTeapot1);
		teapot1.Draw(shader);

		//2. dönüþüm yapýlarak gezegen çizdirilir
		glm::mat4 modelPlanet1 = glm::mat4(1.0f);
		modelPlanet1 = glm::translate(modelPlanet1, glm::vec3(-10.0f, -10.0f, -10.0f));
		modelPlanet1 = glm::scale(modelPlanet1, glm::vec3(0.05f, 0.05f, 0.05f));
		shader.setMat4("model", modelPlanet1);
		planet1.Draw(shader);

		//3. dönüþüm yapýlarak benekli çaydanlýk çizdirilir
		glBindTexture(GL_TEXTURE_2D, texture4);
		glm::mat4 modelTeapot4 = glm::mat4(1.0f);
		modelTeapot4 = glm::translate(modelTeapot4, glm::vec3(10.0f, 10.0f, 10.0f));
		modelTeapot4 = glm::rotate(modelTeapot4, glm::radians(150.0f), glm::vec3(0.0f, 1.0f, 0.0f));
		modelTeapot4 = glm::translate(modelTeapot4, glm::vec3(-10.0f, -10.0f, -10.0f));
		shader.setMat4("model", modelTeapot4);
		teapot4.Draw(shader);

		//4. dönüþüm yapýlarak gezegen çizdirilir
		glm::mat4 modelPlanet2 = glm::mat4(1.0f);
		modelPlanet2 = glm::translate(modelPlanet2, glm::vec3(10.0f, 10.0f, 10.0f));
		modelPlanet2 = glm::scale(modelPlanet2, glm::vec3(0.05f, 0.05f, 0.05f));
		shader.setMat4("model", modelPlanet2);
		planet2.Draw(shader);

		//5. dönüþüm yapýlarak koyu ahþap çaydanlýk çizdirilir
		glBindTexture(GL_TEXTURE_2D, texture3);
		glm::mat4 modelTeapot3 = glm::mat4(1.0f);
		modelTeapot3 = glm::translate(modelTeapot3, glm::vec3(-10.0f, -10.0f, -10.0f));
		modelTeapot3 = glm::scale(modelTeapot3, glm::vec3(0.7f, 0.3f, 0.3f));
		modelTeapot3 = glm::translate(modelTeapot3, glm::vec3(10.0f, 10.0f, 10.0f));
		shader.setMat4("model", modelTeapot3);
		teapot3.Draw(shader);

		//6. dönüþüm yapýlarak koyu mavi çaydanlýk çizdirilir
		glBindTexture(GL_TEXTURE_2D, texture2);
		glm::mat4 modelTeapot2 = glm::mat4(1.0f);
		modelTeapot2 = glm::translate(modelTeapot2, glm::vec3(-1.0f, -1.0f, -1.0f));
		modelTeapot2 = glm::scale(modelTeapot2, glm::vec3(1.0f, 1.0f, -1.0f));
		shader.setMat4("model", modelTeapot2);
		teapot2.Draw(shader);

		//7. dönüþüm yapýlarak kaya çizdirilir
		glm::mat4 modelRock = glm::mat4(1.0f);
		modelRock = glm::translate(modelRock, glm::vec3(-1.0f, -1.0f, -1.0f));
		modelRock = glm::scale(modelRock, glm::vec3(0.05f, 0.05f, 0.05f));
		shader.setMat4("model", modelRock);
		rock.Draw(shader);

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