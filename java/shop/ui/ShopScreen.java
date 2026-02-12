package shop.ui;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.*;

// IMPORTANT: This file takes care of what shop.java would do, but if we see fit,
// the appropriate code will be transfered to that file.

// STEPS TO RUN (type in default terminal in current working directory):
// 1. clear
// 2. javac ShopScreen.java
// 3. java ShopScreen
// 4. clear

// shop/ui is for what the player sees and clicks, pure presentation + input
// shop/ui/ShopScreen is the visual screen for the shop, it has window setup (size, title), bg image loading,
// contd... buttons/clickable things for the items, calls shop.java logic when something is clicked, and displaying text

public class ShopScreen {
    private JLabel statusLabel;
    private int coins = 100; // Starting currency

    public ShopScreen() {
        // 1. Create the main application window (JFrame)
        JFrame frame = new JFrame("Java Shop GUI");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Close operation
        frame.setSize(400, 200); // Set window size
        frame.setLayout(new BorderLayout()); // Use BorderLayout manager

        // 2. Create components (buttons, labels, panels)
        JPanel shopPanel = new JPanel();
        shopPanel.setLayout(new FlowLayout()); // Layout for buttons

        JButton buyItem1Button = new JButton("Buy Item 1 (10 coins)");
        JButton buyItem2Button = new JButton("Buy Item 2 (25 coins)");
        statusLabel = new JLabel("Welcome to the shop! Coins: " + coins, SwingConstants.CENTER); //

        // 3. Add action listeners to buttons
        buyItem1Button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                buyItem(10, "Item 1");
            }
        });

        buyItem2Button.addActionListener(e -> buyItem(25, "Item 2")); // Lambda expression to simplify boilerplate

        // 4. Add components to the panel and frame
        shopPanel.add(buyItem1Button);
        shopPanel.add(buyItem2Button);

        frame.add(statusLabel, BorderLayout.NORTH);
        frame.add(shopPanel, BorderLayout.CENTER);

        // 5. Display the window
        frame.setLocationRelativeTo(null); // Center the window
        frame.setVisible(true); // Make the frame visible
    }

    // Method to handle buying logic
    private void buyItem(int cost, String itemName) {
        if (coins >= cost) {
            coins -= cost;
            statusLabel.setText("You bought " + itemName + "! Coins left: " + coins);
        } else {
            statusLabel.setText("Not enough coins to buy " + itemName + "! Coins: " + coins);
        }
    }

    public static void main(String[] args) {
        // Ensure the GUI creation is done on the Event Dispatch Thread (EDT)
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new ShopScreen();
            }
        });
    }
}
