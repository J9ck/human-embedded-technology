# ⚡ Low-Power Computing for Implantable Devices

> **Power optimization techniques for battery-powered and energy-harvesting implants**

Power is the most critical constraint for implantable devices. This guide covers sleep modes, energy harvesting, power budgeting, and optimization strategies for extending implant lifetime from months to years.

---

## 📋 Table of Contents
- [Power Constraints](#power-constraints)
- [Sleep Modes](#sleep-modes)
- [Dynamic Power Management](#dynamic-power-management)
- [Energy Harvesting](#energy-harvesting)
- [Power Budgeting](#power-budgeting)
- [Optimization Strategies](#optimization-strategies)

---

## 🔋 Power Constraints

### Typical Power Budgets

| Device Type | Power Budget | Battery Life Goal |
|-------------|--------------|-------------------|
| **Passive NFC tag** | 0 µW (powered by reader) | Indefinite |
| **Implantable sensor** | 1-100 µW | 5-10 years |
| **Neural recording** | 100 µW - 1 mW | 1-5 years |
| **Neurostimulator** | 1-10 mW | 6 months - 2 years |
| **Closed-loop BCI** | 5-50 mW | 3-12 months |

### Battery Technologies

| Chemistry | Voltage | Energy Density | Use Case |
|-----------|---------|----------------|----------|
| **Lithium-ion** | 3.7 V | 150-250 Wh/kg | Rechargeable implants |
| **Lithium primary** | 3.0 V | 300-400 Wh/kg | Non-rechargeable, long life |
| **Solid-state** | 3.0 V | 200-300 Wh/kg | Future implants, safer |
| **Zinc-air** | 1.4 V | 400-500 Wh/kg | High density, limited power |

**Example**: 100 mAh battery at 3.7V = 370 mWh = 1332 J
- At 1 mW: 1332 / 1 = 1332 seconds = 370 hours = 15 days
- At 100 µW: 15 days × 10 = 150 days = 5 months
- At 10 µW: 5 months × 10 = 50 months = 4 years

---

## 😴 Sleep Modes

### ARM Cortex-M Power Modes

```c
// STM32 sleep modes
typedef enum {
    MODE_RUN,        // Full operation: ~10 mA at 80 MHz
    MODE_SLEEP,      // CPU stopped, peripherals on: ~5 mA
    MODE_STOP,       // Most peripherals off, RAM retained: 5-50 µA
    MODE_STANDBY     // Everything off except RTC: 0.3-3 µA
} PowerMode_t;

void enter_stop_mode(void) {
    // Configure wakeup source
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
    
    // Disable SysTick to prevent unwanted wakeup
    HAL_SuspendTick();
    
    // Enter STOP mode with low-power regulator
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
    
    // On wakeup, reconfigure system clock
    SystemClock_Config();
    HAL_ResumeTick();
}
```

### Duty Cycling Strategy

```c
// Example: Sample EEG for 100 ms every 10 seconds
#define ACTIVE_TIME_MS   100   // 100 ms acquisition
#define SLEEP_TIME_MS    9900  // 9.9 s sleep
#define DUTY_CYCLE       0.01  // 1%

void main_loop(void) {
    while (1) {
        // Wake up and sample
        adc_start_sampling();
        HAL_Delay(ACTIVE_TIME_MS);
        adc_stop_sampling();
        
        // Process data quickly
        process_eeg_samples();
        
        // Enter deep sleep
        configure_rtc_wakeup(SLEEP_TIME_MS);
        enter_stop_mode();
    }
}

// Average power = Active_Power × Duty_Cycle + Sleep_Power × (1 - Duty_Cycle)
// = 10 mW × 0.01 + 0.01 mW × 0.99 = 0.1 + 0.0099 ≈ 0.11 mW
```

### Wake-Up Sources

```c
// Configure multiple wakeup sources
void configure_wakeup(void) {
    // 1. RTC periodic wakeup (every 10 seconds)
    HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, 10, RTC_WAKEUPCLOCK_CK_SPRE_16BITS);
    
    // 2. External interrupt (e.g., accelerometer motion detect)
    HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
    
    // 3. UART receive (for external commands)
    __HAL_UART_ENABLE_IT(&huart1, UART_IT_RXNE);
}
```

---

## 🎛️ Dynamic Power Management

### Dynamic Voltage and Frequency Scaling (DVFS)

```c
// Scale voltage and frequency based on workload
typedef enum {
    PERF_LOW,      // 4 MHz, 1.8V:   ~1 mA
    PERF_MED,      // 16 MHz, 2.0V:  ~3 mA
    PERF_HIGH,     // 80 MHz, 2.2V:  ~10 mA
    PERF_BOOST     // 120 MHz, 2.4V: ~25 mA
} PerformanceMode_t;

void set_performance_mode(PerformanceMode_t mode) {
    switch (mode) {
        case PERF_LOW:
            HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE2);
            SystemClock_Config_4MHz();
            break;
        case PERF_HIGH:
            HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1);
            SystemClock_Config_80MHz();
            break;
    }
}

// Adaptive performance based on processing needs
void adaptive_performance(void) {
    if (ml_inference_needed) {
        set_performance_mode(PERF_BOOST);  // High frequency for ML
        run_neural_network();
        set_performance_mode(PERF_LOW);    // Back to low power
    }
}
```

### Peripheral Power Management

```c
// Disable unused peripherals
void disable_unused_peripherals(void) {
    // Disable USB
    __HAL_RCC_USB_CLK_DISABLE();
    
    // Disable unused timers
    __HAL_RCC_TIM3_CLK_DISABLE();
    __HAL_RCC_TIM4_CLK_DISABLE();
    
    // Disable GPIO pins (configure as analog input)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Pin = GPIO_PIN_All;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
}
```

---

## 🌱 Energy Harvesting

### Inductive Coupling (Wireless Power)

```
    External Coil               Implanted Coil
    (Transmitter)               (Receiver)
    
    ┌──────────┐                ┌──────────┐
    │          │                │          │
    │   ~~~~   │  Magnetic      │   ~~~~   │
    │  │    │  │    Field       │  │    │  │
    │   ~~~~   │ ────────────→  │   ~~~~   │
    │          │                │          │
    └──────────┘                └──────────┘
         │                           │
         │                           ↓
    AC Source                   Rectifier → Regulator → Load
```

**Characteristics**:
- Frequency: 6.78 MHz, 13.56 MHz, or custom
- Distance: 1-5 cm for implants
- Efficiency: 10-50% depending on alignment
- Power: 1 mW - 1 W

**Circuit**:
```c
// Monitor wireless power receiver
#define POWER_GOOD_THRESHOLD 3.0  // Volts

bool is_wireless_power_available(void) {
    float voltage = read_adc_voltage(VPOWER_ADC_CHANNEL);
    return (voltage > POWER_GOOD_THRESHOLD);
}

// Switch between battery and wireless power
void power_source_management(void) {
    if (is_wireless_power_available()) {
        // Use wireless power, charge battery
        enable_battery_charging();
        power_source = POWER_WIRELESS;
    } else {
        // Fall back to battery
        disable_battery_charging();
        power_source = POWER_BATTERY;
    }
}
```

### Piezoelectric Harvesting

**Motion-Based Energy**:
- Source: Body movement, muscle contractions, heartbeat
- Output: 10-500 µW
- Application: Pacemakers, wearable sensors

```c
// Monitor piezo energy harvester
void piezo_harvesting_monitor(void) {
    float harvested_power = measure_harvested_power();
    
    if (harvested_power > MIN_CHARGING_POWER) {
        enable_supercap_charging();
    }
    
    // Adjust duty cycle based on available energy
    if (supercap_voltage > THRESHOLD_HIGH) {
        increase_sampling_rate();  // More energy available
    } else if (supercap_voltage < THRESHOLD_LOW) {
        decrease_sampling_rate();  // Conserve energy
    }
}
```

### Thermoelectric Harvesting

**Body Heat Conversion**:
- Source: Body-ambient temperature difference (~1-5°C)
- Output: 10-100 µW per cm²
- Challenge: Small temperature gradients in implants

---

## 📊 Power Budgeting

### Example: Neural Recording Implant

```
Component Power Budget:
┌───────────────────────┬──────────┬─────────────┬──────────────┐
│ Component             │ Power    │ Duty Cycle  │ Avg Power    │
├───────────────────────┼──────────┼─────────────┼──────────────┤
│ MCU (active)          │ 10 mW    │ 1%          │ 0.10 mW      │
│ MCU (sleep)           │ 0.01 mW  │ 99%         │ 0.0099 mW    │
│ ADC (8 ch, 1 kHz)     │ 2 mW     │ 10%         │ 0.20 mW      │
│ Amplifier (8 ch)      │ 0.5 mW   │ 100%        │ 0.50 mW      │
│ BLE (transmit)        │ 10 mW    │ 0.1%        │ 0.01 mW      │
│ BLE (idle)            │ 0.005 mW │ 99.9%       │ 0.005 mW     │
│ Flash memory (write)  │ 5 mW     │ 0.01%       │ 0.0005 mW    │
│ Misc (regulators)     │ 0.1 mW   │ 100%        │ 0.10 mW      │
└───────────────────────┴──────────┴─────────────┴──────────────┘
Total Average Power: 0.925 mW ≈ 1 mW

Battery Life Calculation:
Battery: 200 mAh @ 3.7V = 740 mWh
Life = 740 mWh / 1 mW = 740 hours = 31 days
```

### Power Measurement

```c
// Real-time power monitoring
typedef struct {
    float voltage;         // Battery voltage
    float current;         // Current draw
    float power;           // Instantaneous power
    uint32_t energy_used;  // Cumulative energy (mWh)
} PowerMonitor_t;

PowerMonitor_t power_monitor;

void update_power_monitoring(void) {
    power_monitor.voltage = read_battery_voltage();
    power_monitor.current = read_current_sense();
    power_monitor.power = power_monitor.voltage * power_monitor.current;
    
    // Integrate power to get energy (trapezoidal rule)
    static uint32_t last_time = 0;
    uint32_t current_time = HAL_GetTick();
    float dt_hours = (current_time - last_time) / (1000.0 * 3600.0);
    power_monitor.energy_used += power_monitor.power * dt_hours;
    last_time = current_time;
    
    // Log to flash for analysis
    if (current_time % 60000 == 0) {  // Every minute
        log_power_data(&power_monitor);
    }
}
```

---

## ⚡ Optimization Strategies

### 1. **Algorithm Optimization**

```c
// BAD: Floating-point division in loop
for (int i = 0; i < 1000; i++) {
    result[i] = signal[i] / 3.14159;  // Expensive!
}

// GOOD: Precompute reciprocal, use multiplication
float inv_pi = 1.0f / 3.14159f;
for (int i = 0; i < 1000; i++) {
    result[i] = signal[i] * inv_pi;  // 10x faster
}
```

### 2. **DMA for Zero-CPU Data Transfer**

```c
// BAD: CPU copies ADC samples
for (int i = 0; i < 1024; i++) {
    buffer[i] = ADC->DR;  // CPU active, wastes power
}

// GOOD: DMA transfers while CPU sleeps
HAL_ADC_Start_DMA(&hadc, (uint32_t*)buffer, 1024);
__WFI();  // Sleep until DMA complete
```

### 3. **Hardware Acceleration**

```c
// Use hardware CRC instead of software
uint32_t compute_crc(uint8_t *data, uint32_t len) {
    HAL_CRC_Calculate(&hcrc, (uint32_t*)data, len);  // Hardware CRC
    // vs. software loop (100x slower, more power)
}
```

### 4. **Data Compression**

```c
// Compress data before transmission
uint32_t compress_eeg(int16_t *raw, uint8_t *compressed, uint32_t len) {
    // Delta encoding (store differences)
    compressed[0] = raw[0] >> 8;
    compressed[1] = raw[0] & 0xFF;
    
    for (int i = 1; i < len; i++) {
        int16_t delta = raw[i] - raw[i-1];
        compressed[2*i] = delta;  // Often fits in 8 bits
    }
    
    // Result: 50% size reduction → 50% less BLE power
    return len;  // Compressed size
}
```

### 5. **Adaptive Sampling**

```c
// Reduce sampling rate when signal is stable
void adaptive_sampling(void) {
    float signal_variance = calculate_variance(signal_buffer);
    
    if (signal_variance < THRESHOLD_LOW) {
        // Stable signal, reduce sample rate
        set_sample_rate(100);  // 100 Hz
    } else {
        // Active signal, increase sample rate
        set_sample_rate(1000);  // 1 kHz
    }
}
```

---

## 🔗 Related Topics

- [Embedded Systems](embedded-systems.md) - Implement power-saving features
- [Real-Time Systems](real-time-systems.md) - Balance real-time needs with power
- [Power Harvesting](../biomedical-engineering/power-harvesting.md) - BME perspective

**External References**:
- [J9ck/biohacking-wiki](https://github.com/J9ck/biohacking-wiki) - Implant battery safety

---

## 📚 Resources

- **Book**: "Ultra-Low Power Wireless Technologies for Sensor Networks" by B. Zhai
- **Tool**: STM32CubeMX Power Consumption Calculator
- **Tool**: Segger Energy Profiler (J-Link)
- **Datasheet**: Microcontroller power consumption tables

---

[⬅️ Back to CS Index](README.md) | [Next: Real-Time Systems →](real-time-systems.md)
