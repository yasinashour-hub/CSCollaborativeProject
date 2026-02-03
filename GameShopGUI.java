import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.ArrayList;
import java.util.List;

public class GameShopGUI extends JFrame {
    private List<GameItem> items;
    private JTextArea infoArea;
    private JLabel moneyLabel;
    private int playerMoney = 1000; // Starting money

    public GameShopGUI() {
        setTitle("Game Shop");
        setSize(600, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        // Ensure GUI is created on the Event Dispatch Thread (EDT)
        SwingUtilities.invokeLater(this::createGUI);
    }

    private void createGUI() {
        // Initialize components
        items = getShopItems(); // Method to populate shop items
        moneyLabel = new JLabel("Money: " + playerMoney);
        infoArea = new JTextArea();
        infoArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(infoArea);

        // Set up layout
        setLayout(new BorderLayout());

        // Top panel for player stats
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        topPanel.add(moneyLabel);
        add(topPanel, BorderLayout.NORTH);

        // Center panel for shop items (using a GridLayout for a grid layout)
        JPanel shopPanel = new JPanel(new GridLayout(0, 2, 10, 10)); // 2 columns, auto rows, spacing
        for (GameItem item : items) {
            shopPanel.add(createItemPanel(item));
        }
        
        JScrollPane shopScrollPane = new JScrollPane(shopPanel);
        add(shopScrollPane, BorderLayout.CENTER);

        // Bottom panel for information display
        add(scrollPane, BorderLayout.SOUTH);

        setVisible(true);
    }

    private JPanel createItemPanel(GameItem item) {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createLineBorder(Color.BLACK));

        JLabel nameLabel = new JLabel(item.getName());
        JLabel priceLabel = new JLabel("Price: " + item.getPrice());
        JButton buyButton = new JButton("Buy");

        // Add action listener to the button
        buyButton.addActionListener((ActionEvent e) -> {
            // Handle the purchase logic
            if (playerMoney >= item.getPrice()) {
                playerMoney -= item.getPrice();
                moneyLabel.setText("Money: " + playerMoney);
                infoArea.append("Purchased " + item.getName() + " for " + item.getPrice() + " coins.\n");
            } else {
                infoArea.append("Cannot afford " + item.getName() + "!\n");
            }
        });

        panel.add(nameLabel, BorderLayout.NORTH);
        panel.add(new JLabel(item.getDescription()), BorderLayout.CENTER);
        panel.add(priceLabel, BorderLayout.WEST);
        panel.add(buyButton, BorderLayout.EAST);

        return panel;
    }

    private List<GameItem> getShopItems() {
        List<GameItem> shopItems = new ArrayList<>();
        shopItems.add(new GameItem("Racket2.0", 100, " Better Racket"));
        shopItems.add(new GameItem("Racket3.0", 150, " Better Better Racket"));
        shopItems.add(new GameItem("Headbands", 20, " Restores health."));
        shopItems.add(new GameItem("Hat", 300, " Protective gear."));
        return shopItems;
    }

    public static void main(String[] args) {
        new GameShopGUI();
    }
}