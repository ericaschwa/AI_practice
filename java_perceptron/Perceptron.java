/*
       ATTENTION: this file is unfinished. It has been moved to a private repository to be
       finished because it bears similarity to a school project and out of an abundance of
       caution for academic integrity.
*/


import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Scanner;

public class Perceptron
{
    public static void main(String[] args)
    {
        try {
            File file        = new File(args[0]);
            Scanner input    = new Scanner(file);
            int point_size   = input.nextInt();
            int num_points   = input.nextInt();
            int[][] points   = new int[num_points][point_size + 1];
            for (int i = 0; i < num_points; i++) {
                points[i][0] = 1;
                for (int j   = 0; j < point_size; j++) {
                    points[i][j + 1] = input.nextInt();
                }
            }
            for (int i       = 0; i < num_points; i++) {
                for (int j   = 0; j < point_size; j++) {
                    System.out.println(points[i][j]);
                }
            }
            input.close();
            System.out.println("Success!");

        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
