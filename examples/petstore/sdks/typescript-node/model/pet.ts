/**
 * OpenAPI Petstore
 * This is a sample server Petstore server. For this sample, you can use the api key `special-key` to test the authorization filters.
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { RequestFile } from './models';
import { Category } from './category';
import { Tag } from './tag';

/**
* A pet for sale in the pet store
*/
export class Pet {
    'id'?: number;
    'category'?: Category;
    'name': string;
    'photoUrls': Array<string>;
    'tags'?: Array<Tag>;
    /**
    * pet status in the store
    *
    * @deprecated
    */
    'status'?: Pet.StatusEnum;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "id",
            "baseName": "id",
            "type": "number"
        },
        {
            "name": "category",
            "baseName": "category",
            "type": "Category"
        },
        {
            "name": "name",
            "baseName": "name",
            "type": "string"
        },
        {
            "name": "photoUrls",
            "baseName": "photoUrls",
            "type": "Array<string>"
        },
        {
            "name": "tags",
            "baseName": "tags",
            "type": "Array<Tag>"
        },
        {
            "name": "status",
            "baseName": "status",
            "type": "Pet.StatusEnum"
        }    ];

    static getAttributeTypeMap() {
        return Pet.attributeTypeMap;
    }
}

export namespace Pet {
    export enum StatusEnum {
        Available = <any> 'available',
        Pending = <any> 'pending',
        Sold = <any> 'sold'
    }
}
