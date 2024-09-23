import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Job data
const jobData = {
  phoneNumber: '123-456-7890',
  message: 'Hello, this is a notification!',
};

// Create a job in the queue
const job = queue.create('push_notification_code', jobData).save((err) => {
  if (!err) {
    console.log(`Notification job created: ${job.id}`);
  }
});

// Job completion event
job.on('complete', () => {
  console.log('Notification job completed');
});

// Job failure event
job.on('failed', (err) => {
  console.log('Notification job failed');
});
