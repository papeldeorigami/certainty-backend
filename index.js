const util = require('util');
const exec = util.promisify(require('child_process').exec);

const fileUpload = require('express-fileupload');
const express = require('express');
const app = express();
const port = parseInt(process.env.PORT, 10) || 3000;
app.use(fileUpload());

const RECORDING_FILE = 'recording.wav';
const TEMP_FILE = `/tmp/${RECORDING_FILE}`;
const CLASSIFY_COMMAND = './scripts/classify.py'

async function classify() {
    const { stdout, stderr } = await exec(`${CLASSIFY_COMMAND} ${TEMP_FILE}`);
    const results = stdout.trim().split(' ');
    const [ level, label ] = results;
    return { level, label };
}

app.post('/classify', function (req, res, next) {
    console.log('POST /classify');
    let audio_file = req.files[RECORDING_FILE];
    if (!audio_file)
        res.status(500).send({ "error": `Please upload an audio file named ${RECORDING_FILE}` });
    audio_file.mv(`${TEMP_FILE}`, function(err) {
        if (err)
            res.status(500).send(err);
        classify().then((result) => {
            console.log(`Result = ${JSON.stringify(result)}`)
            res.status(201).send(result);
        });
    });
});

app.listen(port, function () {
    console.log(`app listening on port ${port}`)
})
