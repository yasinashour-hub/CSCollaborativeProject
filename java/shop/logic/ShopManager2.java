package shop.logic;
import shop.model.Upgrade;
import java.util.HashSet;
import java.util.Set;
// !!shop/logic/ShopManager.java is the decision maker, it has logic for making purchases, checking it they can afford it, 
// contd... applying the upgrades if successful, and returning success/failure info

class Player {
    int coins;
    Set<String> purchasedOneTimeupgrades = new HashSet<>();

    public Player(int initialCoins) {
        this.coins = initialCoins;
    }
}

class Shop {
    public boolean purchaseupgrade(Player player, Upgrade upgrade) {
        // Check if it's a one-time upgrade and if the player already owns it
        if (upgrade.isOneTimeUse() && player.purchasedOneTimeupgrades.contains(upgrade.getName())) {
            System.out.println("Error: " + upgrade.getName() + " can only be purchased once.");
            return false;
        }

        // Check if the player has enough coins
        if (player.coins >= upgrade.getCost()) {
            player.coins -= upgrade.getCost();
            // Add the upgrade to the player's inventory/purchased upgrades
            if (upgrade.isOneTimeUse()) {
                player.purchasedOneTimeupgrades.add(upgrade.getName());
            }
            System.out.println("Successfully purchased " + upgrade.getName() + "!");
            return true;
        } else {
            System.out.println("Error: Not enough coins to buy " + upgrade.getName() + ".");
            return false;
        }
    }
    
    public int getCoins(Player player) {
        return player.coins;
    }
}
