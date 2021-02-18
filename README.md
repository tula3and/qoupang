# Qoupang

<img src="https://github.com/tula3and/qoupang/blob/main/project_main.png?raw=true" width="700">

- Qiskit Hackathon Project; from [qiskit-hackathon-korea-21](https://github.com/qiskit-community/qiskit-hackathon-korea-21/issues/5)
- Quantum Blockchain Solution for Logistics
- The motivation of this project is
  - security issues in logistic
  - the noise problem in NISQ era
  - to make a real blockchain use case with quantum computing
  - to contribute to the Qiskit community
- Hope this solution used by this event for sucessful SWAG delivery

## How it works

> To deliver Qiskit SWAG (souvenir) properly

1. Get email address from participants
2. Compare it with the email list to check its existence and address
3. Make a block for tracking SWAG delivery
4. Send a mail back to participants to confirm that their email address is correct

## What we did

- Set-up a cloud server using [goorm](https://www.goorm.io/)
- Build QRNG with Qiskit
  - Make random numbers with QRNG (reference: https://www.nature.com/articles/s41598-019-56706-2)
  - Use them to make hash values
- Build a website for participants
  - Input an email
  - Send it with a hash value to make a block
  - Send QRCODE for email authentication

