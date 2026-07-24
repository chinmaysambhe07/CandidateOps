# Security Policy

## 🔒 Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
|---------|-------------------|
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:               |

## 🛡️ Reporting a Vulnerability

If you discover a security vulnerability in CandidateOps, please report it responsibly by:

1. **Do not** create a public GitHub issue
2. **Email** the security team at security@candidateops.example
3. Include as much detail as possible about the vulnerability
4. Provide steps to reproduce if applicable
5. Wait for a response before disclosing publicly

We will acknowledge your report within 48 hours and provide a timeline for resolution.

## 🔐 Security Best Practices

### For Users

- **Never commit sensitive data**: Never commit `.env` files or any files containing credentials
- **Use environment variables**: Store SAP credentials in environment variables, not in code
- **Limit permissions**: Use service accounts with minimal required permissions in SAP
- **Keep dependencies updated**: Regularly run `pip list --outdated` and update packages
- **Monitor logs**: Review application logs for suspicious activity
- **Use secure networks**: Run CandidateOps on trusted, secure networks

### For Developers

- **Input validation**: Validate all inputs from external sources
- **Secure defaults**: Use secure configurations by default
- **Error handling**: Don't expose sensitive information in error messages
- **Dependency scanning**: Regularly check for vulnerabilities in dependencies
- **Code review**: All changes undergo security review during pull request process

## 🧹 Data Handling

CandidateOps handles potentially sensitive personal data. Please ensure:

- **Data minimization**: Only collect and store data necessary for recruitment purposes
- **Data retention**: Establish and follow data retention policies
- **Access control**: Limit access to candidate data to authorized personnel only
- **Secure storage**: Ensure candidate data is stored securely
- **Compliance**: Ensure compliance with relevant data protection regulations (GDPR, CCPA, etc.)

## 📬 Contact

For security-related inquiries, please contact: security@candidateops.example

## 🙏 Acknowledgments

We thank the security researchers and community members who help keep CandidateOps secure.