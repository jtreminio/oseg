/*
 * Redocly Museum API
 * Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.
 *
 * The version of the OpenAPI document: 1.2.1
 * Contact: team@redocly.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


package org.openapimuseum.client.model;

import java.util.Objects;
import com.google.gson.annotations.SerializedName;

import java.io.IOException;
import com.google.gson.TypeAdapter;
import com.google.gson.JsonElement;
import com.google.gson.annotations.JsonAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;

/**
 * Type of ticket being purchased. Use &#x60;general&#x60; for regular museum entry and &#x60;event&#x60; for tickets to special events.
 */
@JsonAdapter(TicketType.Adapter.class)
public enum TicketType {
  
  EVENT("event"),
  
  GENERAL("general");

  private String value;

  TicketType(String value) {
    this.value = value;
  }

  public String getValue() {
    return value;
  }

  @Override
  public String toString() {
    return String.valueOf(value);
  }

  public static TicketType fromValue(String value) {
    for (TicketType b : TicketType.values()) {
      if (b.value.equals(value)) {
        return b;
      }
    }
    throw new IllegalArgumentException("Unexpected value '" + value + "'");
  }

  public static class Adapter extends TypeAdapter<TicketType> {
    @Override
    public void write(final JsonWriter jsonWriter, final TicketType enumeration) throws IOException {
      jsonWriter.value(enumeration.getValue());
    }

    @Override
    public TicketType read(final JsonReader jsonReader) throws IOException {
      String value = jsonReader.nextString();
      return TicketType.fromValue(value);
    }
  }

  public static void validateJsonElement(JsonElement jsonElement) throws IOException {
    String value = jsonElement.getAsString();
    TicketType.fromValue(value);
  }
}

