import kue from 'kue';

const createPushNotificationsJobs = (jobs, queue) => {
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    jobs.forEach(job => {
        const newJob = queue.create('push_notification_code_3', job);

        newJob.save(err => {
            if (!err) {
                console.log(`Notification job created: ${newJob.id}`); // Use newJob.id
            }
        });

        newJob.on('complete', () => {
            console.log(`Notification job ${newJob.id} completed`); // Use newJob.id
        });

        newJob.on('failed', (err) => {
            console.log(`Notification job ${newJob.id} failed: ${err}`); // Use newJob.id
        });

        newJob.on('progress', (progress) => {
            console.log(`Notification job ${newJob.id} ${progress}% complete`); // Use newJob.id
        });
    });
};

export default createPushNotificationsJobs;
