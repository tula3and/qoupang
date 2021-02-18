# Qoupang

- Qiskit Hackathon Project
- Quantum Blockchain Solution for Logistics
- The motivation of this project is
  - security issues in logistic
  - the noise problem in NISQ era
  - to make a real blockchain use case with quantum computing
  - to contribute to the Qiskit community

## How it works

> To deliver Qiskit SWAG (souvenir) properly

1. Get email address from participants
2. Compare it with the email list to check its existence and address
3. Make a block for tracking SWAG delivery
4. Send a mail back to participants to confirm that their email address is correct

## What we did

- Set-up a cloud server using [goorm](https://www.goorm.io/)
- Build QRNG with Qiskit
  - Make random numbers with QRNG
  - Use them to make hash values
- Build a website for participants
  - Input an email
  - Send it with a hash value to make a block
  - Send a confirmation email to the participant

