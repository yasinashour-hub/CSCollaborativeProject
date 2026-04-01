package shop.ui; 
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.*;
import shop.logic.ShopInventory;
import shop.logic.ShopManager;
import shop.model.Upgrade;

// IMPORTANT: This file takes care of what shop.java would do, but if we see fit,
// the appropriate code will be transfered to that file.

// STEPS TO RUN (type in default terminal in project directory):
// 1. clear
// 2. javac ShopScreen.java
// 3. java ShopScreen
// 4. clear

// shop/ui is for what the player sees and clicks, pure presentation + input
// shop/ui/ShopScreen is the visual screen for the shop, it has window setup (size, title), bg image loading,
// contd... buttons/clickable things for the items, calls shop.java logic when something is clicked, and displaying text

public class ShopScreen {
    private Upgrade shoes;
    private Upgrade racket;
    private Upgrade speedPotion;
    private Upgrade powerPotion;
    private Upgrade spinBall;
    private Upgrade pointBall;
    private Upgrade waterBottle;
    private JLabel statusLabel;
    private ShopManager shopManager; // Starting currency

    public ShopScreen() {

        ShopInventory inventory = new ShopInventory(); 
        shoes = inventory.getShoes();
        racket = inventory.getRacket();
        speedPotion = inventory.getSpeedPotion();
        powerPotion = inventory.getPowerPotion();
        spinBall = inventory.getSpinBall();
        pointBall = inventory.getPointBall();
        waterBottle = inventory.getWaterBottle();

        shopManager = new ShopManager(20);
        var boughtracket = 0;
        var boughtshoes = 0;
        var boughtpball = 0;
        var boughtscball = 0;
        var boughtwb = 0;


        // 1. Create the main application window (JFrame)
        JFrame frame = new JFrame("Java Shop GUI");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Close operation
        frame.setSize(400, 200); // Set window size
        frame.setLayout(new BorderLayout()); // Use BorderLayout manager

        // 2. Create components (buttons, labels, panels)
        JPanel shopPanel = new BackgroundPanel("../assets/shop_bg.png");
        shopPanel.setLayout(new GridBagLayout()); // Layout for buttons

        JButton buyShoesButton = 
            new JButton("Buy " + shoes.getName() + " for " + shoes.getCost() + " coins");
        JButton buyRacketButton = 
            new JButton("Buy " + racket.getName() + " for " + racket.getCost() + " coins");
        JButton buyspeedPotionButton =
            new JButton("Buy " + speedPotion.getName() + " for " + speedPotion.getCost() + " coins");
        JButton buypowerPotionButton =
            new JButton("Buy " + powerPotion.getName() + " for " + powerPotion.getCost() + " coins");
        JButton buySpinBallButton =
            new JButton("Buy " + spinBall.getName() + " for " + spinBall.getCost() + " coins");
        JButton buyPointBallButton =
            new JButton("Buy " + pointBall.getName() + " for " + pointBall.getCost() + " coins");
        JButton buyWaterBottleButton =
            new JButton("Buy " + waterBottle.getName() + " for " + waterBottle.getCost() + " coins");

        statusLabel = new JLabel(
            "Welcome to the shop! Coins: " + shopManager.getCoins(), SwingConstants.CENTER); //

        // 3. Add action listeners to buttons
        buyShoesButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(shoes);
                statusLabel.setText(result);
            }
        });

        buyRacketButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(racket);
                statusLabel.setText(result);
            }
        }); // Lambda expression to simplify boilerplate

        buyspeedPotionButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(speedPotion);
                statusLabel.setText(result);
            }
        });

        buypowerPotionButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(powerPotion);
                statusLabel.setText(result);
            }
        });

        buySpinBallButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(spinBall);
                statusLabel.setText(result);
            }
        });

        buyPointBallButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(pointBall);
                statusLabel.setText(result);

            }
        });

        buyWaterBottleButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String result = shopManager.buy(waterBottle);
                statusLabel.setText(result);
            }
        });


        // 4. Add components to the panel and frame
        shopPanel.add(buyShoesButton);
        shopPanel.add(buyRacketButton);
        shopPanel.add(buyspeedPotionButton);
        shopPanel.add(buypowerPotionButton);
        shopPanel.add(buySpinBallButton);
        shopPanel.add(buyPointBallButton);
        shopPanel.add(buyWaterBottleButton);

        frame.add(statusLabel, BorderLayout.NORTH);
        frame.add(shopPanel, BorderLayout.CENTER);
        

        // 5. Display the window
        frame.setLocationRelativeTo(null); // Center the window
        frame.setVisible(true); // Make the frame visible
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new ShopScreen());
    }
}
//Background panel class

class BackgroundPanel extends JPanel {

    private Image background;

    public BackgroundPanel(String path) {
        java.net.URL imgURL = getClass().getResource(path);

        if (imgURL == null) {
            System.out.println("ERROR: Background image not found at " + path);
        } else {
            background = new ImageIcon(imgURL).getImage();
        }
    }


    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(background, 0, 0, getWidth(), getHeight(), this);
    }

}