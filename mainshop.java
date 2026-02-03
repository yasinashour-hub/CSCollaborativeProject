import javax.swing.JFrame;
import javax.swing.JPanel;
import java.awt.Dimension;
public class mainshop {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Upgrade Shop");

        JPanel panel = new JPanel();
        panel.setPreferredSize(new Dimension(1000, 800));

        frame.add(panel);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}