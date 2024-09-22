import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="bg-dark text-light">
      <Container>
        <Row>
          <Col className="text-center py-3">
            <p>
              &copy; 2023 Motor Magic Parts . All rights reserved.| Designed and Developed by Sandip and Sandesh.
            </p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
