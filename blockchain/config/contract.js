const fs = require('fs');
const path = require('path');
const APP_ROOT_DIR = path.join(__dirname, '..');
const Caver = require('caver-js');
const secret = fs.readFileSync(path.join(APP_ROOT_DIR, '.secret.json'));
const parsedSecret = JSON.parse(secret);
const caver = new Caver(parsedSecret.baobab.url);

const metadataOfCO2BoardPPM = fs.readFileSync(path.join(APP_ROOT_DIR, 'metadata/CO2BoardPPM'));
const addressOfCO2BoardPPM = fs.readFileSync(path.join(APP_ROOT_DIR, 'metadata/addressOfCO2BoardPPM'), 'utf-8');
const abiOfCO2BoardPPM = JSON.parse(metadataOfCO2BoardPPM).abi;

const co2BoardPPM = new caver.klay.Contract(abiOfCO2BoardPPM, addressOfCO2BoardPPM);

module.exports = {
    co2BoardPPM: co2BoardPPM 
}