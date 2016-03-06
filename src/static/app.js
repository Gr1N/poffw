require('bootstrap/dist/css/bootstrap.css');
require('./login.css');


var request = require('superagent/lib/client'),
    Parallel = require('paralleljs'),

    form,

    urlLogin = '/login',
    pathEval = '/static/eval.js',
    pathSHA3 = '/static/sha3.js',

    getTask = function(event) {
        form.querySelector('#labelWorking').style.display = '';

        request.get(urlLogin).end(function(err, res) {
            form.querySelector('#inputToken').value = res.header['x-poffw'];

            solveTask(res.body);
        });
    },
    solveTask = function(task) {
        console.log('Got task:', task);
        parallel = new Parallel(task, {
            evalPath: pathEval
        });
        parallel.require(pathSHA3).spawn(solveWorker).then(function(counter) {
            console.log('Task resolved:', counter);

            form.querySelector('#labelWorking').style.display = 'none';
            form.querySelector('#labelSuccess').style.display = '';
            form.querySelector('#inputButton').removeAttribute('disabled');

            form.querySelector('#inputCounter').value = counter;
        });
    },
    solveWorker = function(task) {
        var stamp = [
                task.ver,
                task.bits,
                task.date,
                task.resource,
                task.ext,
                task.rand
            ].join(':'),
            prefix = new Array(task.bits + 1).join('0'),
            counter = 1,

            check = function(counter) {
                var hash = CryptoJS.SHA3([stamp, counter].join(':'));
                return String(hash, {
                    outputLength: 512
                }).indexOf(prefix) === 0;
            };

        while (true) {
            if (check(counter)) {
                return counter;
            }

            counter += 1;
        }
    },

    login = function(event) {
        request.post(urlLogin).set({
            'X-POFFW': form.querySelector('#inputToken').value
        }).send({
            login: form.querySelector('#inputEmail').value,
            password: form.querySelector('#inputPassword').value,
            counter: form.querySelector('#inputCounter').value
        }).end(function(err, res) {
            if (res.statusCode === 200) {
                alert('Success');
            } else {
                alert('Try again');
            }
        });

        event.preventDefault();
    },

    initialize = function() {
        form = document.forms[0];

        form.querySelector('#labelWorking').style.display = 'none';
        form.querySelector('#labelSuccess').style.display = 'none';

        form.addEventListener('submit', login);

        form.querySelector('#inputNotARobot')
            .addEventListener('change', getTask);
    };


initialize();
