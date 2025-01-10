export * from './eventsApi';
import { EventsApi } from './eventsApi';
export * from './operationsApi';
import { OperationsApi } from './operationsApi';
export * from './ticketsApi';
import { TicketsApi } from './ticketsApi';
import * as http from 'http';

export class HttpError extends Error {
    constructor (public response: http.IncomingMessage, public body: any, public statusCode?: number) {
        super('HTTP request failed');
        this.name = 'HttpError';
    }
}

export { RequestFile } from '../model/models';

export const APIS = [EventsApi, OperationsApi, TicketsApi];
