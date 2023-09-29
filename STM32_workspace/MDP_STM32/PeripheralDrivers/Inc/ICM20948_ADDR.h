/**
 * Reference and Inspiration:
 * https://github.com/drcpattison/ICM-20948/blob/master/src/ICM20948.h
 * https://github.com/mokhwasomssi/stm32f4_hal_icm20948_lib/blob/master/mokhwa_ICM20948.h
 * https://github.com/mokhwasomssi/stm32f4_hal_icm20948_lib/blob/master/mokhwa_ICM20948_REGISTER.h
 * 
 * naming convention:
 * device_name__(info__)(name__)Type
 * 
*/
#define ICM20948__I2C_SLAVE_ADDRESS_1 0x68
#define ICM20948__I2C_SLAVE_ADDRESS_2 0x69

#define ICM20948__USER_BANK_ALL__REG_BANK_SEL__REGISTER 0x7F

#define ICM20948__USER_BANK_0__WHO_AM_I__REGISTER 0x00
#define ICM20948__USER_BANK_0__USER_CTRL__REGISTER 0x03
#define ICM20948__USER_BANK_0__LP_CONFIG__REGISTER 0x05
#define ICM20948__USER_BANK_0__PWR_MGMT_1__REGISTER 0x06
#define ICM20948__USER_BANK_0__PWR_MGMT_2__REGISTER 0x07
#define ICM20948__USER_BANK_0__INT_PIN_CFG__REGISTER 0x0F
#define ICM20948__USER_BANK_0__INT_ENABLE__REGISTER 0x10
#define ICM20948__USER_BANK_0__INT_ENABLE_1__REGISTER 0x11
#define ICM20948__USER_BANK_0__INT_ENABLE_2__REGISTER 0x12
#define ICM20948__USER_BANK_0__INT_ENABLE_3__REGISTER 0x13
#define ICM20948__USER_BANK_0__I2C_MST_STATUS__REGISTER 0x17
#define ICM20948__USER_BANK_0__INT_STATUS__REGISTER 0x19
#define ICM20948__USER_BANK_0__INT_STATUS__REGISTER 0x19
#define ICM20948__USER_BANK_0__INT_STATUS_1__REGISTER 0x1A
#define ICM20948__USER_BANK_0__INT_STATUS_2__REGISTER 0x1B
#define ICM20948__USER_BANK_0__INT_STATUS_3__REGISTER 0x1C
#define ICM20948__USER_BANK_0__DELAY_TIMEH__REGISTER 0x28
#define ICM20948__USER_BANK_0__DELAY_TIMEL__REGISTER 0x29
#define ICM20948__USER_BANK_0__ACCEL_XOUT_H__REGISTER 0x2D
#define ICM20948__USER_BANK_0__ACCEL_XOUT_L__REGISTER 0x2E
#define ICM20948__USER_BANK_0__ACCEL_YOUT_H__REGISTER 0x2F
#define ICM20948__USER_BANK_0__ACCEL_YOUT_L__REGISTER 0x30
#define ICM20948__USER_BANK_0__ACCEL_ZOUT_H__REGISTER 0x31
#define ICM20948__USER_BANK_0__ACCEL_ZOUT_L__REGISTER 0x32
#define ICM20948__USER_BANK_0__GYRO_XOUT_H__REGISTER 0x33
#define ICM20948__USER_BANK_0__GYRO_XOUT_L__REGISTER 0x34
#define ICM20948__USER_BANK_0__GYRO_YOUT_H__REGISTER 0x35
#define ICM20948__USER_BANK_0__GYRO_YOUT_L__REGISTER 0x36
#define ICM20948__USER_BANK_0__GYRO_ZOUT_H__REGISTER 0x37
#define ICM20948__USER_BANK_0__GYRO_ZOUT_L__REGISTER 0x38
#define ICM20948__USER_BANK_0__TEMP_OUT_H__REGISTER 0x39
#define ICM20948__USER_BANK_0__TEMP_OUT_L__REGISTER 0x3A
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_00__REGISTER 0x3B
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_01__REGISTER 0x3C
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_02__REGISTER 0x3D
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_03__REGISTER 0x3E
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_04__REGISTER 0x3F
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_05__REGISTER 0x40
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_06__REGISTER 0x41
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_07__REGISTER 0x42
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_08__REGISTER 0x43
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_09__REGISTER 0x44
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_10__REGISTER 0x45
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_11__REGISTER 0x46
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_12__REGISTER 0x47
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_13__REGISTER 0x48
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_14__REGISTER 0x49
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_15__REGISTER 0x4A
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_16__REGISTER 0x4B
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_17__REGISTER 0x4C
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_18__REGISTER 0x4D
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_19__REGISTER 0x4E
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_20__REGISTER 0x4F
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_21__REGISTER 0x50
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_22__REGISTER 0x51
#define ICM20948__USER_BANK_0__EXT_SENS_DATA_23__REGISTER 0x52
#define ICM20948__USER_BANK_0__FIFO_EN_1__REGISTER 0x66
#define ICM20948__USER_BANK_0__FIFO_EN_2__REGISTER 0x67
#define ICM20948__USER_BANK_0__FIFO_RST__REGISTER 0x68
#define ICM20948__USER_BANK_0__FIFO_MODE__REGISTER 0x69
#define ICM20948__USER_BANK_0__FIFO_COUNTH__REGISTER 0x70
#define ICM20948__USER_BANK_0__FIFO_COUNTL__REGISTER 0x71
#define ICM20948__USER_BANK_0__FIFO_R_W__REGISTER 0x72
#define ICM20948__USER_BANK_0__DATA_RDY_STATUS__REGISTER 0x74
#define ICM20948__USER_BANK_0__FIFO_CFG__REGISTER 0x76

#define ICM20948__USER_BANK_1__SELF_TEST_X_GYRO__REGISTER 0x02
#define ICM20948__USER_BANK_1__SELF_TEST_Y_GYRO__REGISTER 0x03
#define ICM20948__USER_BANK_1__SELF_TEST_Z_GYRO__REGISTER 0x04
#define ICM20948__USER_BANK_1__SELF_TEST_X_ACCEL__REGISTER 0x0E
#define ICM20948__USER_BANK_1__SELF_TEST_Y_ACCEL__REGISTER 0x0F
#define ICM20948__USER_BANK_1__SELF_TEST_Z_ACCEL__REGISTER 0x10
#define ICM20948__USER_BANK_1__XA_OFFSET_H__REGISTER 0x14
#define ICM20948__USER_BANK_1__XA_OFFSET_L__REGISTER 0x15
#define ICM20948__USER_BANK_1__YA_OFFSET_H__REGISTER 0x17
#define ICM20948__USER_BANK_1__YA_OFFSET_L__REGISTER 0x18
#define ICM20948__USER_BANK_1__ZA_OFFSET_H__REGISTER 0x1A
#define ICM20948__USER_BANK_1__ZA_OFFSET_L__REGISTER 0x1B
#define ICM20948__USER_BANK_1__TIMEBASE_CORRECTION_PLL__REGISTER 0x28

#define ICM20948__USER_BANK_2__GYRO_SMPLRT_DIV__REGISTER 0x00
#define ICM20948__USER_BANK_2__GYRO_CONFIG_1__REGISTER 0x01
#define ICM20948__USER_BANK_2__GYRO_CONFIG_2__REGISTER 0x02
#define ICM20948__USER_BANK_2__XG_OFFSET_H__REGISTER 0x03
#define ICM20948__USER_BANK_2__XG_OFFSET_L__REGISTER 0x04
#define ICM20948__USER_BANK_2__YG_OFFSET_H__REGISTER 0x05
#define ICM20948__USER_BANK_2__YG_OFFSET_L__REGISTER 0x06
#define ICM20948__USER_BANK_2__ZG_OFFSET_H__REGISTER 0x07
#define ICM20948__USER_BANK_2__ZG_OFFSET_L__REGISTER 0x08
#define ICM20948__USER_BANK_2__ODR_ALIGN_EN__REGISTER 0x09
#define ICM20948__USER_BANK_2__ACCEL_SMPLRT_DIV_1__REGISTER 0x10
#define ICM20948__USER_BANK_2__ACCEL_SMPLRT_DIV_2__REGISTER 0x11
#define ICM20948__USER_BANK_2__ACCEL_INTEL_CTRL__REGISTER 0x12
#define ICM20948__USER_BANK_2__ACCEL_WOM_THR__REGISTER 0x13
#define ICM20948__USER_BANK_2__ACCEL_CONFIG__REGISTER 0x14
#define ICM20948__USER_BANK_2__ACCEL_CONFIG_2__REGISTER 0x15
#define ICM20948__USER_BANK_2__FSYNC_CONFIG__REGISTER 0x52
#define ICM20948__USER_BANK_2__TEMP_CONFIG__REGISTER 0x53
#define ICM20948__USER_BANK_2__MOD_CTRL_USR__REGISTER 0x54

#define ICM20948__USER_BANK_3__I2C_MST_ODR_CONFIG__REGISTER 0x00
#define ICM20948__USER_BANK_3__I2C_MST_CTRL__REGISTER 0x01
#define ICM20948__USER_BANK_3__I2C_MST_DELAY_CTRL__REGISTER 0x02
#define ICM20948__USER_BANK_3__I2C_SLV0_ADDR__REGISTER 0x03
#define ICM20948__USER_BANK_3__I2C_SLV0_REG__REGISTER 0x04
#define ICM20948__USER_BANK_3__I2C_SLV0_CTRL__REGISTER 0x05
#define ICM20948__USER_BANK_3__I2C_SLV0_DO__REGISTER 0x06
#define ICM20948__USER_BANK_3__I2C_SLV1_ADDR__REGISTER 0x07
#define ICM20948__USER_BANK_3__I2C_SLV1_REG__REGISTER 0x08
#define ICM20948__USER_BANK_3__I2C_SLV1_CTRL__REGISTER 0x09
#define ICM20948__USER_BANK_3__I2C_SLV1_DO__REGISTER 0x0A
#define ICM20948__USER_BANK_3__I2C_SLV2_ADDR__REGISTER 0x0B
#define ICM20948__USER_BANK_3__I2C_SLV2_REG__REGISTER 0x0C
#define ICM20948__USER_BANK_3__I2C_SLV2_CTRL__REGISTER 0x0D
#define ICM20948__USER_BANK_3__I2C_SLV2_DO__REGISTER 0x0E
#define ICM20948__USER_BANK_3__I2C_SLV3_ADDR__REGISTER 0x0F
#define ICM20948__USER_BANK_3__I2C_SLV3_REG__REGISTER 0x10
#define ICM20948__USER_BANK_3__I2C_SLV3_CTRL__REGISTER 0x11
#define ICM20948__USER_BANK_3__I2C_SLV3_DO__REGISTER 0x12
#define ICM20948__USER_BANK_3__I2C_SLV4_ADDR__REGISTER 0x13
#define ICM20948__USER_BANK_3__I2C_SLV4_REG__REGISTER 0x14
#define ICM20948__USER_BANK_3__I2C_SLV4_CTRL__REGISTER 0x15
#define ICM20948__USER_BANK_3__I2C_SLV4_DO__REGISTER 0x16
#define ICM20948__USER_BANK_3__I2C_SLV4_DI__REGISTER 0x17