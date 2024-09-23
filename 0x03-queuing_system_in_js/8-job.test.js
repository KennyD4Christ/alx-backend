import kue from 'kue';
import { expect } from 'chai'; // Import expect from chai
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
    before(() => {
        // Enable test mode
        queue.testMode.enter();
    });

    after(() => {
        // Clear the queue and exit test mode
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('should display an error message if jobs is not an array', () => {
        try {
            createPushNotificationsJobs({}, queue);
        } catch (error) {
            expect(error.message).to.equal('Jobs is not an array');
        }
    });

    it('should create two new jobs to the queue', () => {
        const jobs = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account',
            },
            {
                phoneNumber: '1234567890',
                message: 'This is the code 5678 to verify your account',
            },
        ];

        createPushNotificationsJobs(jobs, queue);

        // Check the number of jobs in the queue
        const jobCount = queue.testMode.jobs.length;
        expect(jobCount).to.equal(2);
    });

    afterEach(() => {
        // Clean up jobs after each test
        queue.testMode.clear();
    });
});
