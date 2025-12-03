# 🔧 Embedded Systems for Neural Interfaces

> **Microcontroller programming and firmware development for implantable devices**

Embedded systems form the computational core of neural interfaces and implantable devices. This guide covers microcontroller selection, firmware development, and best practices for resource-constrained medical devices.

---

## 📋 Table of Contents
- [Microcontroller Architectures](#microcontroller-architectures)
- [Development Workflow](#development-workflow)
- [Peripheral Interfaces](#peripheral-interfaces)
- [Memory Management](#memory-management)
- [Interrupt-Driven Programming](#interrupt-driven-programming)
- [Implant-Specific Considerations](#implant-specific-considerations)
- [Example: ADC Sampling](#example-adc-sampling)

---

## 🔬 Microcontroller Architectures

### ARM Cortex-M Series
**Most common for medical implants** due to power efficiency and ecosystem support.

| Core | Features | Use Case |
|------|----------|----------|
| **Cortex-M0/M0+** | Ultra-low power, simple | Passive sensors, NFC tags |
| **Cortex-M4** | DSP instructions, FPU | Biosignal processing |
| **Cortex-M7** | High performance, cache | Real-time ML inference |
| **Cortex-M33** | TrustZone security | Secure medical devices |

**Key Features for Implants**:
- Single-cycle multiply-accumulate (MAC) for DSP
- Hardware floating-point unit (FPU) for signal processing
- Low-power sleep modes (stop, standby)
- DMA for zero-CPU data transfers

### RISC-V
**Emerging open-source alternative** with growing embedded ecosystem.
- Open ISA (no licensing fees)
- Customizable with application-specific extensions
- Small, power-efficient cores
- Limited medical device adoption (yet)

### STM32 Family
**Popular choice for prototyping neural interfaces**:
- **STM32L4**: Ultra-low power, 80 MHz, FPU
- **STM32F4**: High performance, 168 MHz, advanced peripherals
- **STM32WB**: Integrated BLE radio, dual-core
- **STM32H7**: High-end, 480 MHz, Ethernet, advanced DMA

### Nordic nRF Series
**Excellent for wireless implants**:
- **nRF52832**: BLE 5.0, ARM Cortex-M4F, 64 MHz
- **nRF52840**: BLE 5.0, 1 MB Flash, USB, Cortex-M4F
- **nRF5340**: Dual Cortex-M33 cores, advanced BLE features

---

## 🛠️ Development Workflow

### 1. Toolchain Setup
```bash
# Install ARM GCC toolchain
sudo apt install gcc-arm-none-eabi

# Install build tools
sudo apt install cmake ninja-build

# Install debugging tools
sudo apt install gdb-multiarch openocd
```

### 2. Project Structure
```
firmware/
├── src/
│   ├── main.c              # Main application
│   ├── biosignal.c         # Signal acquisition
│   ├── dsp.c               # Signal processing
│   └── wireless.c          # BLE communication
├── inc/
│   └── *.h                 # Header files
├── drivers/
│   └── *.c                 # Hardware drivers
├── lib/
│   └── CMSIS/              # Cortex Microcontroller Software Interface
├── build/                  # Build artifacts
└── platformio.ini          # PlatformIO config
```

### 3. Build and Flash
```bash
# Using PlatformIO
pio run --target upload

# Using OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program build/firmware.elf verify reset exit"
```

---

## 🔌 Peripheral Interfaces

### Analog-to-Digital Converter (ADC)
**Critical for biosignal acquisition**

```c
// Configure ADC for EEG sampling (1 kHz, 12-bit)
void adc_init(void) {
    ADC_HandleTypeDef hadc;
    
    hadc.Instance = ADC1;
    hadc.Init.Resolution = ADC_RESOLUTION_12B;
    hadc.Init.ScanConvMode = DISABLE;
    hadc.Init.ContinuousConvMode = ENABLE;
    hadc.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc.Init.NbrOfConversion = 1;
    
    HAL_ADC_Init(&hadc);
}

// DMA-based continuous sampling
void adc_start_dma(uint16_t *buffer, uint32_t length) {
    HAL_ADC_Start_DMA(&hadc, (uint32_t*)buffer, length);
}
```

**Specifications for Implants**:
- **Resolution**: 12-16 bits for biosignals
- **Sample Rate**: 250 Hz (EEG) to 30 kHz (neural spikes)
- **Input Range**: ±5 mV to ±5 V (with amplification)
- **Power**: <1 mW per channel

### SPI (Serial Peripheral Interface)
**High-speed communication with sensors and accelerators**

```c
// SPI configuration for external ADC (e.g., ADS1299)
SPI_HandleTypeDef hspi;

hspi.Instance = SPI1;
hspi.Init.Mode = SPI_MODE_MASTER;
hspi.Init.Direction = SPI_DIRECTION_2LINES;
hspi.Init.DataSize = SPI_DATASIZE_8BIT;
hspi.Init.CLKPolarity = SPI_POLARITY_LOW;
hspi.Init.CLKPhase = SPI_PHASE_2EDGE;
hspi.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16;

HAL_SPI_Init(&hspi);
```

### I2C (Inter-Integrated Circuit)
**Low-speed communication with sensors (IMU, pressure)**

```c
// I2C configuration for MPU6050 IMU
I2C_HandleTypeDef hi2c;

hi2c.Instance = I2C1;
hi2c.Init.ClockSpeed = 100000;  // 100 kHz standard mode
hi2c.Init.DutyCycle = I2C_DUTYCYCLE_2;
hi2c.Init.OwnAddress1 = 0;
hi2c.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;

HAL_I2C_Init(&hi2c);
```

### UART (Universal Asynchronous Receiver-Transmitter)
**Debugging and low-speed communication**

```c
// UART for debugging output
UART_HandleTypeDef huart;

huart.Instance = USART2;
huart.Init.BaudRate = 115200;
huart.Init.WordLength = UART_WORDLENGTH_8B;
huart.Init.StopBits = UART_STOPBITS_1;
huart.Init.Parity = UART_PARITY_NONE;

HAL_UART_Init(&huart);
```

---

## 💾 Memory Management

### Memory Layout
```
0x08000000 ┌─────────────────┐
           │  Flash (Code)   │  512 KB - 2 MB
           │  - Bootloader   │
           │  - Application  │
           │  - Calibration  │
0x20000000 ├─────────────────┤
           │  SRAM (Data)    │  64 KB - 512 KB
           │  - Stack        │
           │  - Heap         │
           │  - BSS/Data     │
           │  - DMA buffers  │
0x40000000 ├─────────────────┤
           │  Peripherals    │  Memory-mapped
           └─────────────────┘
```

### Stack and Heap Sizing
```c
// In linker script (*.ld)
_Min_Heap_Size = 0x1000;  /* 4 KB for dynamic allocation */
_Min_Stack_Size = 0x800;  /* 2 KB for function calls */

// Stack overflow detection
void check_stack_usage(void) {
    extern uint32_t _estack;
    uint32_t stack_ptr;
    asm("mov %0, sp" : "=r"(stack_ptr));
    
    uint32_t used = _estack - stack_ptr;
    if (used > 0x600) {  // 1.5 KB warning threshold
        handle_stack_overflow();
    }
}
```

### DMA Buffers
```c
// Place DMA buffers in specific memory regions
__attribute__((section(".dma_buffer")))
uint16_t adc_buffer[1024];

// Circular buffer for continuous acquisition
#define BUFFER_SIZE 2048
uint16_t signal_buffer[BUFFER_SIZE];
volatile uint32_t write_index = 0;
volatile uint32_t read_index = 0;
```

---

## ⚡ Interrupt-Driven Programming

### Interrupt Priorities
```c
// Configure NVIC priorities (lower number = higher priority)
HAL_NVIC_SetPriority(ADC_IRQn, 0, 0);      // Highest: ADC sampling
HAL_NVIC_SetPriority(DMA1_Stream0_IRQn, 1, 0);  // DMA transfers
HAL_NVIC_SetPriority(TIM2_IRQn, 2, 0);     // Timer for pacing
HAL_NVIC_SetPriority(USART2_IRQn, 3, 0);   // UART communication

HAL_NVIC_EnableIRQ(ADC_IRQn);
```

### Interrupt Service Routine (ISR)
```c
// ADC conversion complete callback
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    uint16_t sample = HAL_ADC_GetValue(hadc);
    
    // Store in circular buffer (fast, no blocking)
    signal_buffer[write_index++] = sample;
    if (write_index >= BUFFER_SIZE) {
        write_index = 0;
    }
    
    // Set flag for main loop processing
    new_sample_ready = 1;
}

// Keep ISRs SHORT - defer processing to main loop
```

### Atomic Operations
```c
// Protect shared variables from race conditions
#include <stdatomic.h>

atomic_uint_fast32_t sample_count = ATOMIC_VAR_INIT(0);

void ADC_IRQHandler(void) {
    atomic_fetch_add(&sample_count, 1);
}
```

---

## 🔬 Implant-Specific Considerations

### Low-Power Modes
```c
// Enter stop mode between sampling windows
void enter_low_power(void) {
    // Configure wakeup source (RTC, external interrupt)
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
    
    // Enter STOP mode (peripherals off, RAM retained)
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
    
    // Upon wakeup, reconfigure clocks
    SystemClock_Config();
}
```

### Watchdog Timer
```c
// Reset system if firmware hangs (critical for implants)
IWDG_HandleTypeDef hiwdg;

void watchdog_init(void) {
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_64;
    hiwdg.Init.Reload = 4095;  // ~8 second timeout
    HAL_IWDG_Init(&hiwdg);
}

void watchdog_refresh(void) {
    HAL_IWDG_Refresh(&hiwdg);
}
```

### Error Handling
```c
// Graceful error recovery
void Error_Handler(void) {
    // Log error to non-volatile memory
    log_error_to_flash();
    
    // Attempt recovery
    HAL_NVIC_SystemReset();
    
    // If critical, enter safe mode
    while(1) {
        // Blink LED, disable stimulation, wait for external reset
    }
}
```

---

## 💡 Example: ADC Sampling for EEG

```c
#include "stm32f4xx_hal.h"

#define SAMPLE_RATE 1000  // 1 kHz for EEG
#define BUFFER_SIZE 256

ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;
TIM_HandleTypeDef htim2;

uint16_t adc_buffer[BUFFER_SIZE];
volatile uint8_t buffer_ready = 0;

// Initialize ADC with DMA and timer trigger
void eeg_adc_init(void) {
    // ADC configuration
    hadc1.Instance = ADC1;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConv = ADC_EXTERNALTRIGCONV_T2_TRGO;
    hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_RISING;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    HAL_ADC_Init(&hadc1);
    
    // DMA configuration
    hdma_adc1.Instance = DMA2_Stream0;
    hdma_adc1.Init.Channel = DMA_CHANNEL_0;
    hdma_adc1.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_adc1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_adc1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_adc1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
    hdma_adc1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_adc1.Init.Mode = DMA_CIRCULAR;
    hdma_adc1.Init.Priority = DMA_PRIORITY_HIGH;
    HAL_DMA_Init(&hdma_adc1);
    
    __HAL_LINKDMA(&hadc1, DMA_Handle, hdma_adc1);
    
    // Timer configuration for 1 kHz sampling
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 84 - 1;  // 84 MHz / 84 = 1 MHz
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 1000 - 1;  // 1 MHz / 1000 = 1 kHz
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    HAL_TIM_Base_Init(&htim2);
    
    TIM_MasterConfigTypeDef sMasterConfig = {0};
    sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
    sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
    HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig);
}

// Start continuous acquisition
void eeg_start_acquisition(void) {
    HAL_TIM_Base_Start(&htim2);
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, BUFFER_SIZE);
}

// DMA transfer complete callback
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    buffer_ready = 1;  // Signal main loop to process buffer
}

// Main processing loop
int main(void) {
    HAL_Init();
    SystemClock_Config();
    eeg_adc_init();
    eeg_start_acquisition();
    
    while (1) {
        if (buffer_ready) {
            buffer_ready = 0;
            
            // Process EEG data (filtering, feature extraction)
            process_eeg_data(adc_buffer, BUFFER_SIZE);
            
            // Send via BLE or store locally
            transmit_data();
        }
        
        // Enter low-power mode between processing
        __WFI();  // Wait for interrupt
    }
}
```

---

## 🔗 Related Topics

- [Signal Processing](signal-processing.md) - Filter EEG data from ADC
- [Real-Time Systems](real-time-systems.md) - RTOS for complex firmware
- [Low-Power Computing](low-power-computing.md) - Optimize power consumption
- [Wireless Protocols](wireless-protocols.md) - Transmit data via BLE

**External References**:
- [J9ck/AI](https://github.com/J9ck/AI) - ML models for biosignal classification
- [J9ck/biohacking-wiki](https://github.com/J9ck/biohacking-wiki) - Hardware implants

---

## 📚 Resources

- **Documentation**: ARM Cortex-M4 Programming Manual
- **Tools**: STM32CubeMX for peripheral configuration
- **Frameworks**: Zephyr RTOS, Mbed OS
- **Debugging**: Segger J-Link, OpenOCD

---

[⬅️ Back to CS Index](README.md) | [Next: Signal Processing →](signal-processing.md)
