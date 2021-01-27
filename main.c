/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
CAN_HandleTypeDef hcan1;

/* USER CODE BEGIN PV */
//uint8_t ubKeyNumber = 0x0;
//CAN_HandleTypeDef     CanHandle;
//CAN_TxHeaderTypeDef   TxHeader;
//CAN_RxHeaderTypeDef   RxHeader;
uint8_t ubKeyNumber = 0x0;
CAN_HandleTypeDef     CanHandle;
CAN_TxHeaderTypeDef   TxHeader;
CAN_RxHeaderTypeDef   RxHeader;
uint8_t               TxData[8];
uint8_t               TxData1[8];
uint8_t               TxData2[8];
uint8_t               TxData3[8];
uint8_t               TxData4[8];
uint8_t               RxData[8];
uint32_t              TxMailbox;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_CAN1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
typedef struct Command { // (1)
  uint8_t P_term;
  uint8_t I_term;
  uint8_t D_term;
  uint8_t speed1;
  uint8_t speed2;
  uint8_t speed3;
  uint8_t throwerSpeed;
  uint8_t delimiter; // (2)
} Command;

typedef struct Feedback { // (3)
  int16_t speed1;
  int16_t speed2;
  int16_t speed3;
  uint16_t delimiter;
} Feedback;


Command command = {.P_term = 25, .I_term = 25, .D_term = 0, .speed1 = 65, .speed2 = 65, .speed3 = 65, .throwerSpeed = 0, .delimiter = 0}; // (4)
volatile uint8_t isCommandReceived = 0; // (5)

void CDC_On_Receive(uint8_t* buffer, uint32_t* length) { // (6)
	if (*length == sizeof(Command)) { // (7)
    memcpy(&command, buffer, sizeof(Command)); // (8)
    if (command.delimiter == 0xAA) { // (9)
      isCommandReceived = 1;
    }
  }
}

unsigned int float_to_uint(float x, float x_min, float x_max, int bits){
	float span = x_max - x_min;
	float offset = x_min;
	unsigned int pgg = 0;
	if(bits == 12){
		pgg = (unsigned int)((x-offset)*4095.0/span);
	}
	if(bits == 16){
		pgg = (unsigned int)((x-offset)*65535.0/span);
	}
	return pgg;
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	  Feedback feedback = { // (1)
	      .speed1 = 0,
	      .speed2 = 0,
	      .speed3 = 0,
	      .delimiter = 0xAAAA
	  };
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
  DWT->CYCCNT = 0;
  DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;

  unsigned long t1 = DWT->CYCCNT;

  int drv_en = 0;
  int loendur = 0;

  unsigned long servotimer = DWT->CYCCNT;
  unsigned long servotimer2 = DWT->CYCCNT;

  uint8_t PRL_speed = 40;

  uint8_t ball_state = 0;

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */
  unsigned int p_int = float_to_uint(0.0f, -12.5f, 12.5f, 16); //las ta olla muidu tulevad errorid, tglt ei kasutda teda

  unsigned int v_int = float_to_uint((float)(command.speed1 - 65), -65.0f, 65.0f, 12);
  unsigned int kp_int = float_to_uint(command.P_term / 25., 0.0f, 10.0f, 12);
  unsigned int kd_int = float_to_uint(command.D_term / 25., 0.0f, 10.0f, 12);
  unsigned int t_int = float_to_uint(command.I_term / 25., 0.0f, 10.0f, 12);
  /* Set the data to be transmitted */
  TxData1[0] = p_int >> 8;
  TxData1[1] = p_int & 0xFF;
  TxData1[2] = v_int >> 4;
  TxData1[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  TxData1[4] = kp_int & 0xFF;
  TxData1[5] = kd_int >> 4;
  TxData1[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  TxData1[7] = t_int & 0xFF;

  v_int = float_to_uint((float)(command.speed2 - 65), -65.0f, 65.0f, 12);

  TxData2[0] = p_int >> 8;
  TxData2[1] = p_int & 0xFF;
  TxData2[2] = v_int >> 4;
  TxData2[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  TxData2[4] = kp_int & 0xFF;
  TxData2[5] = kd_int >> 4;
  TxData2[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  TxData2[7] = t_int & 0xFF;

  v_int = float_to_uint((float)(command.speed3 - 65), -65.0f, 65.0f, 12);

  TxData3[0] = p_int >> 8;
  TxData3[1] = p_int & 0xFF;
  TxData3[2] = v_int >> 4;
  TxData3[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  TxData3[4] = kp_int & 0xFF;
  TxData3[5] = kd_int >> 4;
  TxData3[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  TxData3[7] = t_int & 0xFF;

  /*
  v_int = float_to_uint((float)(command.throwerSpeed - 65), -65.0f, 65.0f, 12);

  TxData4[0] = p_int >> 8;
  TxData4[1] = p_int & 0xFF;
  TxData4[2] = v_int >> 4;
  TxData4[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  TxData4[4] = kp_int & 0xFF;
  TxData4[5] = kd_int >> 4;
  TxData4[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  TxData4[7] = t_int & 0xFF;
  */
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USB_DEVICE_Init();
  //while(isCommandReceived == 0); //halb aga hea
  MX_CAN1_Init();
  /* USER CODE BEGIN 2 */
  //HAL_Delay(1000);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  if((DWT->CYCCNT - servotimer) / 60000 > 20){
		  servotimer = DWT->CYCCNT;
		  HAL_GPIO_WritePin(ESC_GPIO_Port, ESC_Pin, 1);
		  while((DWT->CYCCNT - servotimer) / 60 < (command.throwerSpeed * 7.69 + 1000));
		  HAL_GPIO_WritePin(ESC_GPIO_Port, ESC_Pin, 0);
	  }


/*
	  if((DWT->CYCCNT - servotimer2) / 60000 > 20){
		  servotimer2 = DWT->CYCCNT;
		  HAL_GPIO_WritePin(PRL_GPIO_Port, PRL_Pin, 1);
		  while((DWT->CYCCNT - servotimer2) / 60 < (PRL_speed * 7.69 + 1000));
		  HAL_GPIO_WritePin(PRL_GPIO_Port, PRL_Pin, 0);
	  }

	  */


	  //võta seeialist uus data vastu ja pistab selle CAN buffritesse
	  if (isCommandReceived) { // (2)

		  //CDC_Transmit_FS(&feedback, sizeof(feedback)); // (5)
		  CDC_Transmit_FS(&ball_state, sizeof(ball_state));

	      isCommandReceived = 0;

	  //    if(command.throwerSpeed > 0) PRL_speed = 0;
	  //    else PRL_speed = 40;


	      p_int = float_to_uint(0.0f, -12.5f, 12.5f, 16); //las ta olla muidu tulevad errorid, tglt ei kasutda teda

	      v_int = float_to_uint((float)(command.speed1 - 65), -65.0f, 65.0f, 12);
	      kp_int = float_to_uint(command.P_term / 25., 0.0f, 10.0f, 12);
	      kd_int = float_to_uint(command.D_term / 25., 0.0f, 10.0f, 12);
	      t_int = float_to_uint(command.I_term / 25., 0.0f, 10.0f, 12);
	      /* Set the data to be transmitted */
	      TxData1[0] = p_int >> 8;
	      TxData1[1] = p_int & 0xFF;
	      TxData1[2] = v_int >> 4;
	      TxData1[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
	      TxData1[4] = kp_int & 0xFF;
	      TxData1[5] = kd_int >> 4;
	      TxData1[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
	      TxData1[7] = t_int & 0xFF;

	      v_int = float_to_uint((float)(command.speed2 - 65), -65.0f, 65.0f, 12);

	      TxData2[0] = p_int >> 8;
	      TxData2[1] = p_int & 0xFF;
	      TxData2[2] = v_int >> 4;
	      TxData2[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
	      TxData2[4] = kp_int & 0xFF;
	      TxData2[5] = kd_int >> 4;
	      TxData2[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
	      TxData2[7] = t_int & 0xFF;

	      v_int = float_to_uint((float)(command.speed3 - 65), -65.0f, 65.0f, 12);

	      TxData3[0] = p_int >> 8;
	      TxData3[1] = p_int & 0xFF;
	      TxData3[2] = v_int >> 4;
	      TxData3[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
	      TxData3[4] = kp_int & 0xFF;
	      TxData3[5] = kd_int >> 4;
	      TxData3[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
	      TxData3[7] = t_int & 0xFF;

/*
	      v_int = float_to_uint((float)(command.throwerSpeed - 65), -65.0f, 65.0f, 12);

	      TxData4[0] = p_int >> 8;
	      TxData4[1] = p_int & 0xFF;
	      TxData4[2] = v_int >> 4;
	      TxData4[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
	      TxData4[4] = kp_int & 0xFF;
	      TxData4[5] = kd_int >> 4;
	      TxData4[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
	      TxData4[7] = t_int & 0xFF;
*/
	      HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin); // (3)
	      //CDC_Transmit_FS(&diff_time, sizeof(diff_time));
	      //CDC_Transmit_FS(TxData, sizeof(TxData)); // (5)

	  }

	  //see osa stardib timeri
	  if(command.speed1 == 65 && command.speed2 == 65 && command.speed3 == 65){
		  if(loendur == 0){
			  loendur = 1;
			  t1 = DWT->CYCCNT;  // reseti loendur
		  }
	  }
	  else{
		  enable:
		  loendur = 0;
		  if(drv_en == 0){
			  //see osa enable kontrollerid kui kiirused ei ole nullis
				  drv_en = 1;

				  TxData[0] = 0xFF;
				  TxData[1] = 0xFF;
				  TxData[2] = 0xFF;
				  TxData[3] = 0xFF;
				  TxData[4] = 0xFF;
				  TxData[5] = 0xFF;
				  TxData[6] = 0xFF;
				  TxData[7] = 0xFC;

				  TxHeader.StdId = 0x01;
			  	  TxHeader.ExtId = 0x01;
			  	  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  /* Transmission request Error */
				  	  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
				  	  drv_en = 0;
				  	  goto enable;
			  	  }
			  	  HAL_Delay(100);
			  	  TxHeader.StdId = 0x02;
			  	  TxHeader.ExtId = 0x02;
			  	  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  /* Transmission request Error */
				  	  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
				  	  drv_en = 0;
				  	goto enable;
			  	  }
			  	  HAL_Delay(100);
			  	  TxHeader.StdId = 0x03;
			  	  TxHeader.ExtId = 0x03;
			  	  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  /* Transmission request Error */
			  		  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
			  		  drv_en = 0;
			  		  goto enable;
			  	  }
			  	  /*
			  	  HAL_Delay(100);
			  	  TxHeader.StdId = 0x04;
			  	  TxHeader.ExtId = 0x04;
			  	  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  // Transmission request Error
			  		  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
			  		  drv_en = 0;
			  		  goto enable;
			  	  }
			  	  */
			  HAL_Delay(50);
		  }
	  }

	  //see osa disableb kontrollerid peale 5 sekundit
	  unsigned long t2 = DWT->CYCCNT;
	  unsigned long diff_time = (t2 - t1) / 60000000;
	  if(diff_time > 5 && loendur == 1){							//tsükkel iga pmst 5 sec tagant kui loendur on starditud

		  disable:

		  if((command.speed1 == 65 && command.speed2 == 65 && command.speed3 == 65) && drv_en == 1){ //saada stop kui mootorid seisma peaksid
			  drv_en = 0;

			  TxData[0] = 0xFF;
			  TxData[1] = 0xFF;
			  TxData[2] = 0xFF;
			  TxData[3] = 0xFF;
			  TxData[4] = 0xFF;
			  TxData[5] = 0xFF;
			  TxData[6] = 0xFF;
			  TxData[7] = 0xFD;

			  TxHeader.StdId = 0x01;
			  TxHeader.ExtId = 0x01;
			  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  /* Transmission request Error */
			  	HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
			  	drv_en = 1;
			  	goto disable;
			  }
			  HAL_Delay(100);
			  TxHeader.StdId = 0x02;
			  TxHeader.ExtId = 0x02;
			  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  /* Transmission request Error */
			  	HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
			  	drv_en = 1;
			  	goto disable;
			  }
			  HAL_Delay(100);
			  TxHeader.StdId = 0x03;
			  TxHeader.ExtId = 0x03;
			  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  /* Transmission request Error */
			  	HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
			  	drv_en = 1;
			  	goto disable;
			  }
			  /*
			  HAL_Delay(100);
			  TxHeader.StdId = 0x04;
			  TxHeader.ExtId = 0x04;
			  if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData, &TxMailbox) != HAL_OK){
			  	  // Transmission request Error
			  	HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
			  	drv_en = 1;
			  	goto disable;
			  }
		  */
			  HAL_Delay(40);

		  }
	  }

	  //kui thrower on nullis, nulli ära balli staatus
	  if(command.throwerSpeed == 0){
		  ball_state = 0;
	  }

	  	 //should use interrupts but nahhh
	  if(HAL_GPIO_ReadPin(BALL_GPIO_Port, BALL_Pin)){
		  ball_state = 1;
	  }


  	  if(drv_en == 1){
	  //see osa saadab info igale driverile
	  TxHeader.StdId = 0x01;
	  TxHeader.ExtId = 0x01;
      if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData1, &TxMailbox) != HAL_OK){
    	  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
    	  //Error_Handler();
      }
	  TxHeader.StdId = 0x02;
	  TxHeader.ExtId = 0x02;
      if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData2, &TxMailbox) != HAL_OK){
    	  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
    	  //Error_Handler();
      }
	  TxHeader.StdId = 0x03;
	  TxHeader.ExtId = 0x03;
      if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData3, &TxMailbox) != HAL_OK){
    	  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
    	  //Error_Handler();
      }
      HAL_Delay(10);
      /*
      HAL_Delay(30);
	  TxHeader.StdId = 0x04;
	  TxHeader.ExtId = 0x04;
      if (HAL_CAN_AddTxMessage(&CanHandle, &TxHeader, TxData4, &TxMailbox) != HAL_OK){
    	  HAL_CAN_AbortTxRequest(&CanHandle, &TxMailbox);
    	  //Error_Handler();
      }
      */
  	  }


  }
}
  /* USER CODE END 3 */

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);
  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 60;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 3;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_CLK48;
  PeriphClkInitStruct.PLLSAI.PLLSAIM = 4;
  PeriphClkInitStruct.PLLSAI.PLLSAIN = 96;
  PeriphClkInitStruct.PLLSAI.PLLSAIQ = 2;
  PeriphClkInitStruct.PLLSAI.PLLSAIP = RCC_PLLSAIP_DIV4;
  PeriphClkInitStruct.PLLSAIDivQ = 1;
  PeriphClkInitStruct.Clk48ClockSelection = RCC_CLK48CLKSOURCE_PLLSAIP;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief CAN1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_CAN1_Init(void)
{

	  CAN_FilterTypeDef  sFilterConfig;

	  /*##-1- Configure the CAN peripheral #######################################*/
	  CanHandle.Instance = CAN1;

	  CanHandle.Init.TimeTriggeredMode = DISABLE;
	  CanHandle.Init.AutoBusOff = DISABLE;
	  CanHandle.Init.AutoWakeUp = DISABLE;
	  CanHandle.Init.AutoRetransmission = ENABLE;
	  CanHandle.Init.ReceiveFifoLocked = DISABLE;
	  CanHandle.Init.TransmitFifoPriority = DISABLE;
	  CanHandle.Init.Mode = CAN_MODE_NORMAL;
	  CanHandle.Init.SyncJumpWidth = CAN_SJW_1TQ;
	  CanHandle.Init.TimeSeg1 = CAN_BS1_8TQ;
	  CanHandle.Init.TimeSeg2 = CAN_BS2_6TQ;
	  CanHandle.Init.Prescaler = 2;

	  if (HAL_CAN_Init(&CanHandle) != HAL_OK)
	  {
	    /* Initialization Error */
	    Error_Handler();
	  }

  /* USER CODE BEGIN CAN1_Init 2 */
  /*##-2- Configure the CAN Filter ###########################################*/
    sFilterConfig.FilterBank = 0;
    sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
    sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
    sFilterConfig.FilterIdHigh = 0x0000;
    sFilterConfig.FilterIdLow = 0x0000;
    sFilterConfig.FilterMaskIdHigh = 0x0000;
    sFilterConfig.FilterMaskIdLow = 0x0000;
    sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
    sFilterConfig.FilterActivation = ENABLE;
    sFilterConfig.SlaveStartFilterBank = 14;

    if (HAL_CAN_ConfigFilter(&CanHandle, &sFilterConfig) != HAL_OK)
    {
      /* Filter configuration Error */
      Error_Handler();
    }

    /*##-3- Start the CAN peripheral ###########################################*/
    if (HAL_CAN_Start(&CanHandle) != HAL_OK)
    {
      /* Start Error */
      Error_Handler();
    }

    /*##-4- Activate CAN RX notification #######################################*/
    if (HAL_CAN_ActivateNotification(&CanHandle, CAN_IT_RX_FIFO0_MSG_PENDING) != HAL_OK)
    {
      /* Notification Error */
      Error_Handler();
    }

    /*##-5- Configure Transmission process #####################################*/
    TxHeader.StdId = 0x01;
    TxHeader.ExtId = 0x01;
    TxHeader.RTR = CAN_RTR_DATA;
    TxHeader.IDE = CAN_ID_STD;
    TxHeader.DLC = 8;
    TxHeader.TransmitGlobalTime = DISABLE;

  /* USER CODE END CAN1_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */

/* USER CODE BEGIN 4 */


void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
  /* Get RX message */
  if (HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData) != HAL_OK)
  {
    /* Reception Error */
    Error_Handler();
  }

  /* Display LEDx */
  if ((RxHeader.StdId == 0x321) && (RxHeader.IDE == CAN_ID_STD) && (RxHeader.DLC == 2))
  {
    LED_Display(RxData[0]);
    ubKeyNumber = RxData[0];
  }
}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(ESC_GPIO_Port, ESC_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(PRL_GPIO_Port, PRL_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : LED_Pin */
  GPIO_InitStruct.Pin = LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LED_GPIO_Port, &GPIO_InitStruct);

  // config for esc pin
  GPIO_InitStruct.Pin = ESC_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ESC_GPIO_Port, &GPIO_InitStruct);

  // config for prl pin
  GPIO_InitStruct.Pin = PRL_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(PRL_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : PB6 PB7 */
  GPIO_InitStruct.Pin = GPIO_PIN_6|GPIO_PIN_7;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : BALL */
    GPIO_InitStruct.Pin = BALL_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(BALL_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
