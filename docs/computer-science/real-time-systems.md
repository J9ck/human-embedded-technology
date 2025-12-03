# ⏱️ Real-Time Systems for Neural Interfaces

> **RTOS concepts and deterministic execution for closed-loop neuromodulation**

Real-time systems are essential for applications requiring guaranteed response times, such as closed-loop brain stimulation, prosthetic control, and time-critical biosignal processing.

---

## 📋 Table of Contents
- [Real-Time Requirements](#real-time-requirements)
- [Real-Time Operating Systems](#real-time-operating-systems)
- [Task Scheduling](#task-scheduling)
- [Interrupt Handling](#interrupt-handling)
- [Inter-Task Communication](#inter-task-communication)
- [Example Implementation](#example-implementation)

---

## ⏰ Real-Time Requirements

### Hard vs. Soft Real-Time

| Type | Deadline Tolerance | Consequences | Example |
|------|-------------------|--------------|---------|
| **Hard RT** | Must never miss | System failure, harm | Pacemaker, closed-loop stim |
| **Firm RT** | Occasional miss OK | Degraded performance | Video streaming |
| **Soft RT** | Best effort | User inconvenience | UI responsiveness |

### Neural Interface Timing Requirements

```
Application          | Latency Requirement | Type
---------------------|--------------------|---------
Closed-loop stim     | <10 ms             | Hard RT
Prosthetic control   | <50 ms             | Firm RT
BCI cursor control   | <100 ms            | Soft RT
EEG visualization    | <500 ms            | Soft RT
Data logging         | <1 s               | Soft RT
```

---

## 🔧 Real-Time Operating Systems

### Popular RTOS for Implants

#### FreeRTOS
**Most popular, open-source, permissive license**

```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

// Task priorities (higher number = higher priority)
#define PRIORITY_ADC_SAMPLING    4  // Highest
#define PRIORITY_SIGNAL_PROC     3
#define PRIORITY_BLE_TX          2
#define PRIORITY_LOGGING         1  // Lowest

void vTaskADCSampling(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xPeriod = pdMS_TO_TICKS(1);  // 1 ms period
    
    for (;;) {
        // Sample ADC at precise 1 kHz rate
        uint16_t sample = read_adc();
        xQueueSend(xQueueADC, &sample, 0);
        
        // Delay until next 1 ms boundary
        vTaskDelayUntil(&xLastWakeTime, xPeriod);
    }
}

int main(void) {
    // Create queue for inter-task communication
    xQueueADC = xQueueCreate(128, sizeof(uint16_t));
    
    // Create high-priority ADC sampling task
    xTaskCreate(vTaskADCSampling, "ADC", 128, NULL, PRIORITY_ADC_SAMPLING, NULL);
    
    // Start scheduler
    vTaskStartScheduler();
    
    // Should never reach here
    for (;;);
}
```

#### Zephyr RTOS
**Modern, scalable, Linux Foundation project**

```c
#include <zephyr.h>

#define STACK_SIZE 1024
#define PRIORITY_ADC 5

K_THREAD_STACK_DEFINE(adc_stack, STACK_SIZE);
struct k_thread adc_thread;

void adc_sampling_thread(void *arg1, void *arg2, void *arg3) {
    while (1) {
        uint16_t sample = adc_read();
        process_sample(sample);
        
        k_sleep(K_MSEC(1));  // 1 ms period
    }
}

int main(void) {
    k_thread_create(&adc_thread, adc_stack, STACK_SIZE,
                    adc_sampling_thread, NULL, NULL, NULL,
                    PRIORITY_ADC, 0, K_NO_WAIT);
    
    return 0;
}
```

---

## 📊 Task Scheduling

### Priority-Based Preemptive Scheduling

```
Time →
Task 1 (High)   ████░░░░░░████░░░░░░
Task 2 (Med)    ░░░░██░░░░░░░░██░░░░
Task 3 (Low)    ░░░░░░██░░░░░░░░░███
Idle            ░░░░░░░░██░░░░░░░░░░

Legend: █ = Running, ░ = Ready/Blocked
```

**Preemption**: Higher priority task always runs first

```c
// Example: Closed-loop stimulation
void vTaskStimControl(void *pvParameters) {
    // HIGHEST PRIORITY - must respond quickly
    for (;;) {
        // Wait for EEG spike detection
        uint32_t notification;
        xTaskNotifyWait(0, 0xFFFFFFFF, &notification, portMAX_DELAY);
        
        // Trigger stimulation immediately (<1 ms from detection)
        trigger_stimulation();
        
        // Latency analysis
        uint32_t latency = get_timestamp() - notification;
        log_latency(latency);
    }
}
```

### Rate Monotonic Scheduling
**Optimal for periodic tasks**: Shorter period = higher priority

```c
// Task periods and priorities
// T1: 10 ms → Priority 3 (highest)
// T2: 20 ms → Priority 2
// T3: 50 ms → Priority 1 (lowest)

void create_periodic_tasks(void) {
    xTaskCreate(vTaskSignalProc, "SP", 256, NULL, 3, NULL);   // 10 ms
    xTaskCreate(vTaskBLE, "BLE", 256, NULL, 2, NULL);         // 20 ms
    xTaskCreate(vTaskLogging, "LOG", 256, NULL, 1, NULL);     // 50 ms
}
```

---

## ⚡ Interrupt Handling

### ISR Design for Real-Time Systems

```c
// BAD: Too much work in ISR
void ADC_IRQHandler(void) {
    uint16_t sample = ADC->DR;
    
    // Don't do this in ISR!
    filter_sample(sample);
    process_sample(sample);
    send_via_ble(sample);
}

// GOOD: Minimal ISR, defer to task
QueueHandle_t xQueueADC;

void ADC_IRQHandler(void) {
    uint16_t sample = ADC->DR;
    
    // Just store sample and signal task
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xQueueSendFromISR(xQueueADC, &sample, &xHigherPriorityTaskWoken);
    
    // Request context switch if needed
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

void vTaskSignalProcessing(void *pvParameters) {
    uint16_t sample;
    for (;;) {
        // Wait for sample from ISR
        if (xQueueReceive(xQueueADC, &sample, portMAX_DELAY)) {
            // Do heavy processing in task context
            filter_sample(sample);
            process_sample(sample);
        }
    }
}
```

### Interrupt Priorities and Latency

```c
// Configure interrupt priorities (lower number = higher priority)
NVIC_SetPriority(ADC_IRQn, 0);          // Highest: data acquisition
NVIC_SetPriority(TIMER_IRQn, 1);        // Timing critical
NVIC_SetPriority(DMA_IRQn, 2);          // Data transfer
NVIC_SetPriority(UART_IRQn, 3);         // Communication
NVIC_SetPriority(SysTick_IRQn, 15);     // Lowest: OS tick

// Measure interrupt latency
void ADC_IRQHandler(void) {
    GPIO_SetBits(GPIOA, GPIO_Pin_0);  // Debug pin high
    
    // ISR code here (minimal processing)
    uint16_t sample = ADC->DR;
    process_sample_quickly(sample);
    
    GPIO_ResetBits(GPIOA, GPIO_Pin_0);  // Debug pin low
    // Measure pulse width on oscilloscope
}
```

---

## 📡 Inter-Task Communication

### Queues (Producer-Consumer)

```c
// Safe data passing between tasks
QueueHandle_t xQueueSamples;

void vTaskProducer(void *pvParameters) {
    for (;;) {
        uint16_t sample = acquire_sample();
        
        // Send to queue (blocks if full)
        xQueueSend(xQueueSamples, &sample, portMAX_DELAY);
        
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}

void vTaskConsumer(void *pvParameters) {
    uint16_t sample;
    for (;;) {
        // Receive from queue (blocks if empty)
        if (xQueueReceive(xQueueSamples, &sample, portMAX_DELAY)) {
            process_sample(sample);
        }
    }
}
```

### Semaphores (Synchronization)

```c
SemaphoreHandle_t xSemaphoreDataReady;

void vTaskAcquisition(void *pvParameters) {
    for (;;) {
        acquire_data_block();
        
        // Signal that data is ready
        xSemaphoreGive(xSemaphoreDataReady);
        
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void vTaskProcessing(void *pvParameters) {
    for (;;) {
        // Wait for data ready signal
        xSemaphoreTake(xSemaphoreDataReady, portMAX_DELAY);
        
        // Process data
        process_data_block();
    }
}
```

### Direct Task Notifications (Fastest)

```c
TaskHandle_t xTaskStimHandle;

void spike_detection_callback(void) {
    // Notify stimulation task (from ISR or task)
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    vTaskNotifyGiveFromISR(xTaskStimHandle, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

void vTaskStimulation(void *pvParameters) {
    for (;;) {
        // Wait for notification (ultra-low latency)
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        // Respond immediately
        trigger_stimulation();
    }
}
```

---

## 💡 Example: Closed-Loop Neural Stimulation

```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

// System configuration
#define SAMPLE_RATE        1000     // 1 kHz
#define DETECTION_THRESHOLD 100     // µV
#define STIM_DELAY_MS      5        // Target <10 ms

// Task handles
TaskHandle_t xTaskADCHandle;
TaskHandle_t xTaskDetectionHandle;
TaskHandle_t xTaskStimHandle;

// Queue for samples
QueueHandle_t xQueueSamples;

// 1. ADC Sampling Task (Highest Priority)
void vTaskADCSampling(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xPeriod = pdMS_TO_TICKS(1);  // 1 ms
    
    for (;;) {
        // Sample neural signal
        int16_t sample = read_neural_adc();
        
        // Send to detection task
        xQueueSend(xQueueSamples, &sample, 0);
        
        // Precise 1 kHz sampling
        vTaskDelayUntil(&xLastWakeTime, xPeriod);
    }
}

// 2. Spike Detection Task (High Priority)
void vTaskSpikeDetection(void *pvParameters) {
    int16_t sample;
    int16_t filtered_sample;
    
    for (;;) {
        // Receive sample
        if (xQueueReceive(xQueueSamples, &sample, portMAX_DELAY)) {
            // Apply bandpass filter (300 Hz - 3 kHz)
            filtered_sample = bandpass_filter(sample);
            
            // Check for threshold crossing
            if (abs(filtered_sample) > DETECTION_THRESHOLD) {
                // Spike detected! Notify stimulation task
                xTaskNotifyGive(xTaskStimHandle);
            }
        }
    }
}

// 3. Stimulation Task (Highest Priority)
void vTaskStimulation(void *pvParameters) {
    for (;;) {
        // Wait for spike detection notification
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        // Trigger stimulation immediately
        uint32_t start_time = get_timestamp_us();
        trigger_pulse();
        uint32_t latency = get_timestamp_us() - start_time;
        
        // Log latency for analysis
        log_stim_latency(latency);
        
        // Refractory period (prevent repeated triggering)
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

int main(void) {
    // Hardware initialization
    init_hardware();
    
    // Create queue
    xQueueSamples = xQueueCreate(16, sizeof(int16_t));
    
    // Create tasks with appropriate priorities
    xTaskCreate(vTaskADCSampling, "ADC", 128, NULL, 4, &xTaskADCHandle);
    xTaskCreate(vTaskSpikeDetection, "DET", 256, NULL, 3, &xTaskDetectionHandle);
    xTaskCreate(vTaskStimulation, "STIM", 128, NULL, 5, &xTaskStimHandle);
    
    // Start scheduler
    vTaskStartScheduler();
    
    // Should never reach here
    for (;;);
}
```

---

## 📈 Worst-Case Execution Time (WCET)

### Measuring and Bounding WCET

```c
// Use timer to measure task execution time
void vTaskCritical(void *pvParameters) {
    for (;;) {
        uint32_t start = TIM2->CNT;
        
        // Critical task code
        critical_processing();
        
        uint32_t end = TIM2->CNT;
        uint32_t execution_time = end - start;
        
        // Log worst case
        if (execution_time > worst_case_time) {
            worst_case_time = execution_time;
        }
        
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

---

## 🔗 Related Topics

- [Embedded Systems](embedded-systems.md) - Hardware platform
- [Low-Power Computing](low-power-computing.md) - Power vs. real-time trade-offs
- [Closed-Loop Systems](../integration/closed-loop-systems.md) - Application example

**External References**:
- [J9ck/AI](https://github.com/J9ck/AI) - Real-time ML inference

---

## 📚 Resources

- **Book**: "Real-Time Systems" by Jane W. S. Liu
- **RTOS**: FreeRTOS documentation
- **RTOS**: Zephyr Project
- **Tool**: Tracealyzer for RTOS profiling

---

[⬅️ Back to CS Index](README.md) | [Next: Wireless Protocols →](wireless-protocols.md)
