public class playground {
    public static void main(String[] args) {

        String game = "";
        int s = 0;
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 4; j++) {
                for (int k = 7; k < 15; k++) {
                    if (i == 0) {
                        game = "s";
                        if (j == 0) {
                            System.out.print("\"" + game + "-c-" + k + "\": " + s + ",");
                            s++;
                        } else if (j == 1) {
                            System.out.print("\"" + game + "-d-" + k + "\": " + s + ",");
                            s++;
                        } else if (j == 2) {
                            System.out.print("\"" + game + "-h-" + k + "\": " + s + ",");
                            s++;
                        } else {
                            System.out.print("\"" + game + "-s-" + k + "\": " + s + ",");
                            s++;
                        }
                    } else {
                        game = "h";
                        if (j == 0) {
                            System.out.print("\"" + game + "-c-" + k + "\": " + s + ",");
                            s++;
                        } else if (j == 1) {
                            System.out.print("\"" + game + "-d-" + k + "\": " + s + ",");
                            s++;
                        } else if (j == 2) {
                            System.out.print("\"" + game + "-h-" + k + "\": " + s + ",");
                            s++;
                        } else {
                            System.out.print("\"" + game + "-s-" + k + "\": " + s + ",");
                            s++;
                        }
                    }
                }
            }
        }
    }
}