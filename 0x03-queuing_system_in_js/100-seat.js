import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const PORT = 1245;

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Kue queue
const queue = kue.createQueue();

// Initialize available seats and reservation status
const INITIAL_SEATS = 50;
let reservationEnabled = true;

// Set initial available seats in Redis
setAsync('available_seats', INITIAL_SEATS);

// Function to reserve seats
const reserveSeat = (number) => {
    return setAsync('available_seats', number);
};

// Function to get current available seats
const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return parseInt(seats, 10);
};

// Route to get available seats
app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservations are blocked' });
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (!err) {
            return res.json({ status: 'Reservation in process' });
        }
        return res.json({ status: 'Reservation failed' });
    });
});

// Process the queue
app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        try {
            const currentSeats = await getCurrentAvailableSeats();
            if (currentSeats > 0) {
                await reserveSeat(currentSeats - 1);
                if (currentSeats - 1 === 0) {
                    reservationEnabled = false;
                }
                console.log(`Seat reservation job ${job.id} completed`);
                done();
            } else {
                done(new Error('Not enough seats available'));
            }
        } catch (error) {
            console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
            done(error);
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
