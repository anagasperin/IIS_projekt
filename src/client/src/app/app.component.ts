import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NetworkService } from './network.service';
import { lastValueFrom } from 'rxjs';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  @ViewChild('chartCanvas')
  chartCanvas?: ElementRef<HTMLCanvasElement>;
  currentWeather: any;
  bikeAvailability: any;
  forecast: any;

  constructor(private networkService: NetworkService) {}

  ngOnInit(): void {
    this.getData();
  }

  async getData() {
    this.currentWeather = await lastValueFrom(
      this.networkService.getCurrentWeather()
    );
    this.bikeAvailability = await lastValueFrom(
      this.networkService.getBikeAvailability()
    );
    this.forecast = await lastValueFrom(this.networkService.getForecast());

    if (this.chartCanvas != undefined && this.forecast != undefined) {
      console.log(this.forecast.vehicles_available);
      this.getChart(this.chartCanvas.nativeElement);
    }
  }

  async getChart(element: HTMLCanvasElement) {
    new Chart(element, {
      type: 'bar',
      data: {
        labels: this.forecast.date,
        datasets: [
          {
            label: 'Bike availability by hour',
            data: this.forecast.vehicles_available,
          },
        ],
      },
    });
  }
}
