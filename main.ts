import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-metadata-form',
  templateUrl: './metadata-form.component.html',
  styleUrls: ['./metadata-form.component.scss']
})
export class MetadataFormComponent implements OnInit {
  metadata = {
    contributors: '',
    title: '',
    institution: '',
    release_year: null,
    doi: '',
    dataset_type: '',
    version: '',
    keywords: '',
    contributor_roles: '',
    language: '',
    alternate_identifiers: '',
    related_publications: '',
    timeline: '',
    file_formats: '',
    dataset_size: '',
    licensing: '',
    funding_reference: '',
    collection_location: '',
    description: '',
    processed: '',
    system: '',
    preprocessing: '',
    numsubjects: null,
    studies: '',
    experiment: '',
    instruments: '',
    Keys: '',
    datapoints: null,
    bpms: '',
    numbpms: null,
    updown: '',
    movements: '',
    movementskey: '',
    prepost: '',
    lprepost: '',
    bow_stroke: ''
  };

  metadataList: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadMetadata();
  }

  submitMetadata() {
    this.http.post('http://127.0.0.1:5000/submit-metadata', this.metadata)
      .subscribe(response => {
        alert("Metadata submitted successfully!");
        this.loadMetadata(); // Refresh the metadata list after submission
      });
  }

  loadMetadata() {
    this.http.get('http://127.0.0.1:5000/get-metadata')
      .subscribe(response => {
        this.metadataList = response as any[];
      });
  }
}
