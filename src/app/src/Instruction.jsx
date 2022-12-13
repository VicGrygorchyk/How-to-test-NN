import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import catPlaceholder from './assets/cat-placeholder.svg';
import { ApiClient } from './api/apiClient';
import "./Instruction.css";

export class Instruction extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image: catPlaceholder,
      isCat: 'Тут з\'явиться результат',
    };
    this.onImageChange = this.onImageChange.bind(this);
    this.handleSelectedImg = this.handleSelectedImg.bind(this);
    this.apiClient = new ApiClient();
  }

  onImageChange(event) {
    if (event.target.files && event.target.files[0]) {
      let reader = new FileReader();
      reader.onload = (e) => {
        this.setState({ image: e.target.result });
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  };

  async handleSelectedImg(event) {
    event.preventDefault();
    try {
      const body = {
          src: this.state.image,
      }
      const resp = await this.apiClient.classifyCat(body);
      console.log('=== isCat ' + resp);

      this.setState(state => ({
        image: state.image,
        isCat: resp.is_cat ? 'Це кіт!': 'Не схоже на кота!',
      }));
    } catch (err) {
      console.log(err);
      this.setState(state => ({
        image: catPlaceholder,
        isCat: 'Помилка',
      }));
    }
  }

  render() {
    return (
      <Row className="instruction">
        <h3>Мережа 1: кіт чи собака?</h3>
        <Col>
          <Form onSubmit={this.handleSelectedImg}>
            <Form.Group className="mb-3">
              <Form.Control
                name="catImage"
                type="file"
                size="lg"
                onChange={this.onImageChange}
              />
            </Form.Group>
            <button type="submit" className="translate-btn">Перевірити фото на котячість</button>
          </Form>
        </Col>
        <Col>
          <img id="preview" alt="cat placeholder" src={ this.state.image } />
        </Col>
        <Col>
          <div><h3>{this.state.isCat}</h3></div>
        </Col>
      </Row>
    );
  }
}
