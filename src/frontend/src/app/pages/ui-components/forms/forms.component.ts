import { Component } from "@angular/core";

import { HttpClient } from  '@angular/common/http';

@Component({
  selector: "app-forms",
  templateUrl: "./forms.component.html",
  styleUrl: "./forms.component.scss",
})

export class AppFormsComponent {
  fileName = "";

  constructor(private http: HttpClient) {}

  onFileSelected(event:any) {
    const file: File = event.target.files[0];

    if (file) {
      this.fileName = file.name;

      const formData = new FormData();

      formData.append("thumbnail", file);

      const upload$ = this.http.post("/api/thumbnail-upload", formData);

      upload$.subscribe();
    }
  }
}
