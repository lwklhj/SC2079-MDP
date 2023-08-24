package org.ntu.controller;
import com.fazecast.jSerialComm.*;
import org.ntu.model.Movement;

public class SerialComHandler {
    private static final String portDescriptor = "/dev/ttyUSBx";
    private static final int baudRate = 115200;
    private static SerialPort serialPort = null;

    public static void setUp() {
        serialPort = SerialPort.getCommPort(portDescriptor);
        // Set parameters
        serialPort.setBaudRate(baudRate);
        //serialPort.setFlowControl();
        //serialPort.set
        //serialPort.setParity();
        //serialPort.setNumStopBits();
        //serialPort.setNumDataBits();
        serialPort.openPort();
    }

    public static void close() {
        serialPort.closePort();
    }

    public static void sendMovementCommand(Movement movement) {
        byte[] bytes = new byte[]{};
        serialPort.writeBytes(bytes, bytes.length);
    }

    public static void addDataListener(Runnable function) {
        function.run();
    }
}