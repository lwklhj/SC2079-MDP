package org.ntu.model;

public class OccupancyGridMap {
    private boolean[][] map;
    private int MAX_X, MAX_Y;

    public OccupancyGridMap(int x, int y) {
        map = new boolean[x][y];
    }
    public void markOccupied(int posX, int posY, int margin) {
        int posXMin = posX - margin;
        int posXMax = posX + margin;
        int posYMin = posY - margin;
        int posYMax = posY + margin;
        for(int x = posXMin; x < posXMax; x++) {
            for(int y = posYMin; y < posYMax; y++) {
                map[x][y] = true;
            }
        }
    }

    public void markEmpty(int posX, int posY, int margin) {
        int posXMin = posX - margin;
        int posXMax = posX + margin;
        int posYMin = posY - margin;
        int posYMax = posY + margin;
        for(int x = posXMin; x < posXMax; x++) {
            for(int y = posYMin; y < posYMax; y++) {
                map[x][y] = false;
            }
        }
    }

    public boolean checkOccupied(int x, int y) {
        return map[x][y];
    }
}