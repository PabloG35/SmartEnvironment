import React, { useState, useEffect } from "react";
import {
  IonPage,
  IonContent,
  IonGrid,
  IonRow,
  IonCol,
  IonButton,
  IonFooter,
  IonTabBar,
  IonTabButton,
  IonIcon,
  IonLabel,
} from "@ionic/react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import { home, timeOutline, person } from "ionicons/icons";
import "./Dashboard.css";

const Dashboard: React.FC = () => {
  const minTemp = 10;
  const maxTemp = 35;
  
  // Initialize temperature state (default value may be 22 or null)
  const [temperature, setTemperature] = useState<number>(22);

  // Calculate gauge values based on the current temperature
  const gaugeValue = temperature - minTemp;
  const gaugeMax = maxTemp - minTemp;

  // Placeholder fixed values for other gauges
  const lightValue = 0;
  const soundValue = 0;
  const gasValue = 0;

  const halfCircleStyles = buildStyles({
    rotation: 0.75,
    trailColor: "#d6d6d6",
    textColor: "#333",
  });

  // Use useEffect to fetch the live temperature from the backend API every 5 seconds.
  useEffect(() => {
    const fetchTemperature = async () => {
      try {

        const response = await fetch("http://127.0.0.1:5000/live_temperature");
        const data = await response.json();
        if (response.ok && data.temperature !== undefined) {
          setTemperature(data.temperature);
        } else {
          console.error("Error fetching temperature:", data.error);
        }
      } catch (error) {
        console.error("Error fetching temperature:", error);
      }
    };

    fetchTemperature();
    const interval = setInterval(fetchTemperature, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <IonPage>
      <IonContent className="container" fullscreen>
        <IonGrid>
          {/* Row 1: Temperature Gauge & Sleep Mode Button */}
          <IonRow className="dashboard-row row-1">
            <IonCol className="gauge-col">
              <div className="gauge-container">
                <div className="gauge-arc-container">
                  <CircularProgressbar
                    value={gaugeValue}
                    maxValue={gaugeMax}
                    text={`${temperature}°C`}
                    circleRatio={0.5}
                    styles={halfCircleStyles}
                  />
                </div>
                <div className="gauge-label">Temperature</div>
              </div>
            </IonCol>
            <IonCol className="button-col">
              <IonButton className="sleep-mode-button">Sleep Mode</IonButton>
            </IonCol>
          </IonRow>

          {/* Row 2: Light, Sound, Air Quality Gauges */}
          <IonRow className="dashboard-row row-2">
            <IonCol className="gauge-col">
              <div className="gauge-container">
                <CircularProgressbar
                  value={lightValue}
                  maxValue={100}
                  text={`${lightValue}%`}
                  circleRatio={0.5}
                  styles={halfCircleStyles}
                />
                <div className="gauge-label">Light</div>
              </div>
            </IonCol>

            <IonCol className="gauge-col">
              <div className="gauge-container">
                <CircularProgressbar
                  value={soundValue}
                  maxValue={100}
                  text={`${soundValue}%`}
                  circleRatio={0.5}
                  styles={halfCircleStyles}
                />
                <div className="gauge-label">Sound</div>
              </div>
            </IonCol>

            <IonCol className="gauge-col">
              <div className="gauge-container">
                <CircularProgressbar
                  value={gasValue}
                  maxValue={100}
                  text={`${gasValue}%`}
                  circleRatio={0.5}
                  styles={halfCircleStyles}
                />
                <div className="gauge-label">Air Quality</div>
              </div>
            </IonCol>
          </IonRow>
        </IonGrid>
      </IonContent>

      <IonFooter className="custom-footer">
        <IonTabBar slot="bottom">
          <IonTabButton tab="home">
            <IonIcon icon={home} />
            <IonLabel>Home</IonLabel>
          </IonTabButton>
          <IonTabButton tab="history">
            <IonIcon icon={timeOutline} />
            <IonLabel>History</IonLabel>
          </IonTabButton>
          <IonTabButton tab="profile">
            <IonIcon icon={person} />
            <IonLabel>Profile</IonLabel>
          </IonTabButton>
        </IonTabBar>
      </IonFooter>
    </IonPage>
  );
};

export default Dashboard;
