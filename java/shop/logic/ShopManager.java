package shop.logic;
import shop.model.Upgrade;
import java.util.HashSet;
import java.util.Set;
// !!shop/logic/ShopManager.java is the decision maker, it has logic for making purchases, checking it they can afford it, 
// contd... applying the upgrades if successful, and returning success/failure info
public class ShopManager {

    private int coins;
    Set<String> purchasedOneTimeItems = new HashSet<>();

    public ShopManager(int startingCoins) {
        this.coins = startingCoins;
    }

    public boolean canAfford(Upgrade upgrade) {
        return coins >= upgrade.getCost();
    }

    public String buy(Upgrade upgrade) {
        if (canAfford(upgrade)) {
            coins -= upgrade.getCost();
            // Here you would apply the upgrade's effects to the player
            return "You bought " + upgrade.getName() + "! Coins left: " + coins;
        } else {
            return "Not enough coins to buy " + upgrade.getName() + "! Coins: " + coins;
        }

    }
    public int getCoins() {
            return coins;
        }
}
