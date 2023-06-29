import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class NetworkService {
  constructor(private httpClient: HttpClient) {}

  getCurrentWeather(): Observable<any> {
    const lat = '46.55472';
    const lon = '15.64667';
    const key = '87c05a0a8d8ea08172b92485c4a60cde';
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${key}&units=metric`;
    return this.httpClient.get<any>(url).pipe(
      catchError((error): any => {
        alert('Network error');
        return { error: error };
      })
    );
  }

  getBikeAvailability(): Observable<any> {
    const url = `"https://api.modra.ninja/jcdecaux/maribor/stations"`;
    return this.httpClient.get<any>(url).pipe(
      catchError((error): any => {
        alert('Network error');
        return { error: error };
      })
    );
  }

  getForecast(): Observable<any> {
    const url = 'http://localhost:5000/forecast';
    return this.httpClient.get<any>(url).pipe(
      catchError((error): any => {
        alert('Network error');
        console.log(error);
        return { error: error };
      })
    );
  }
}
