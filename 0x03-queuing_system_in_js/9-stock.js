import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const PORT = 1245;

// Products list
const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);

// Function to get item by ID
const getItemById = (id) => {
    return listProducts.find(product => product.id === id);
};

// Route to list all products
app.get('/list_products', (req, res) => {
    const products = listProducts.map(({ id, name, price, stock }) => ({
        itemId: id,
        itemName: name,
        price,
        initialAvailableQuantity: stock,
    }));
    res.json(products);
});

// Route to get product details
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);

    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock,
        currentQuantity: currentQuantity || 0,
    });
});

// Function to reserve stock by ID
const reserveStockById = (itemId, stock) => {
    redisClient.set(`item.${itemId}`, stock);
};

// Function to get current reserved stock by ID
const getCurrentReservedStockById = async (itemId) => {
    const stock = await getAsync(`item.${itemId}`);
    return stock ? parseInt(stock, 10) : 0;
};

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);

    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const currentStock = await getCurrentReservedStockById(itemId);
    if (currentStock >= product.stock) {
        return res.json({
            status: 'Not enough stock available',
            itemId: product.id,
        });
    }

    reserveStockById(itemId, currentStock + 1);
    res.json({
        status: 'Reservation confirmed',
        itemId: product.id,
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
