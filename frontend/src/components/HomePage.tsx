import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import Alert from "react-bootstrap/Alert";
import { useState } from "react";
import axios from "axios";

const HomePage = () => {
  const [searchText, setSearchText] = useState("");
  const [baconDistance, setBaconDistance] = useState<number | null>(null);
  const [actorName, setActorName] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const getActorBaconDistance = (searchedActorName: string) => {
    setIsLoading(true);
    axios
      .get(
        `http://localhost:8000/bacon-distance?actor_name=${searchedActorName}`,
      )
      .then((response) => {
        const baconDistance = response.data.bacon_distance;
        const actorName = response.data.actor;
        setBaconDistance(baconDistance ?? Infinity);
        setActorName(actorName);
        setErrorMessage(null);
      })
      .catch((error) => {
        setBaconDistance(null);
        setActorName(null);
        setErrorMessage(error.response?.data?.detail || "Something went wrong");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };
  return (
    <Container className="mt-5" style={{ maxWidth: "600px" }}>
      <Card className="p-4 shadow-sm">
        <h1 className="mb-3 text-center">Bacon Distance Calculator</h1>
        <p className="text-muted text-center">
          Find how far any actor is from Kevin Bacon!
        </p>

        <Form
          onSubmit={(e) => {
            e.preventDefault();
            getActorBaconDistance(searchText);
          }}
        >
          <Form.Group className="mb-3">
            <Form.Label>Actor Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter full name"
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
            />
          </Form.Group>

          <Button variant="primary" type="submit" className="w-100" disabled={isLoading}>
            {isLoading ? "Calculating..." : "Calculate"}
          </Button>
        </Form>

        {baconDistance !== null && actorName !== null && (
          <Alert variant="success" className="mt-4">
            <strong>{actorName}</strong>'s Bacon distance is{" "}
            <strong>{baconDistance}</strong>
          </Alert>
        )}

        {errorMessage != null && (
          <Alert variant="danger" className="mt-4">
            {errorMessage}
          </Alert>
        )}
      </Card>
    </Container>
  );
};

export default HomePage;
