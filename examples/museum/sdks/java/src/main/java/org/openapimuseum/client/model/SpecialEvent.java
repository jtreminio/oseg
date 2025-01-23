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
import com.google.gson.TypeAdapter;
import com.google.gson.annotations.JsonAdapter;
import com.google.gson.annotations.SerializedName;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.TypeAdapterFactory;
import com.google.gson.reflect.TypeToken;
import com.google.gson.TypeAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import java.io.IOException;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.openapimuseum.client.JSON;

/**
 * SpecialEvent
 */
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", comments = "Generator version: 7.11.0")
public class SpecialEvent {
  public static final String SERIALIZED_NAME_EVENT_ID = "eventId";
  @SerializedName(SERIALIZED_NAME_EVENT_ID)
  @javax.annotation.Nullable
  private UUID eventId;

  public static final String SERIALIZED_NAME_NAME = "name";
  @SerializedName(SERIALIZED_NAME_NAME)
  @javax.annotation.Nonnull
  private String name;

  public static final String SERIALIZED_NAME_LOCATION = "location";
  @SerializedName(SERIALIZED_NAME_LOCATION)
  @javax.annotation.Nonnull
  private String location;

  public static final String SERIALIZED_NAME_EVENT_DESCRIPTION = "eventDescription";
  @SerializedName(SERIALIZED_NAME_EVENT_DESCRIPTION)
  @javax.annotation.Nonnull
  private String eventDescription;

  public static final String SERIALIZED_NAME_DATES = "dates";
  @SerializedName(SERIALIZED_NAME_DATES)
  @javax.annotation.Nonnull
  private List<LocalDate> dates = new ArrayList<>();

  public static final String SERIALIZED_NAME_PRICE = "price";
  @SerializedName(SERIALIZED_NAME_PRICE)
  @javax.annotation.Nonnull
  private Float price;

  public SpecialEvent() {
  }

  public SpecialEvent eventId(@javax.annotation.Nullable UUID eventId) {
    this.eventId = eventId;
    return this;
  }

  /**
   * Identifier for a special event.
   * @return eventId
   */
  @javax.annotation.Nullable
  public UUID getEventId() {
    return eventId;
  }

  public void setEventId(@javax.annotation.Nullable UUID eventId) {
    this.eventId = eventId;
  }


  public SpecialEvent name(@javax.annotation.Nonnull String name) {
    this.name = name;
    return this;
  }

  /**
   * Name of the special event.
   * @return name
   */
  @javax.annotation.Nonnull
  public String getName() {
    return name;
  }

  public void setName(@javax.annotation.Nonnull String name) {
    this.name = name;
  }


  public SpecialEvent location(@javax.annotation.Nonnull String location) {
    this.location = location;
    return this;
  }

  /**
   * Location where the special event is held.
   * @return location
   */
  @javax.annotation.Nonnull
  public String getLocation() {
    return location;
  }

  public void setLocation(@javax.annotation.Nonnull String location) {
    this.location = location;
  }


  public SpecialEvent eventDescription(@javax.annotation.Nonnull String eventDescription) {
    this.eventDescription = eventDescription;
    return this;
  }

  /**
   * Description of the special event.
   * @return eventDescription
   */
  @javax.annotation.Nonnull
  public String getEventDescription() {
    return eventDescription;
  }

  public void setEventDescription(@javax.annotation.Nonnull String eventDescription) {
    this.eventDescription = eventDescription;
  }


  public SpecialEvent dates(@javax.annotation.Nonnull List<LocalDate> dates) {
    this.dates = dates;
    return this;
  }

  public SpecialEvent addDatesItem(LocalDate datesItem) {
    if (this.dates == null) {
      this.dates = new ArrayList<>();
    }
    this.dates.add(datesItem);
    return this;
  }

  /**
   * List of planned dates for the special event.
   * @return dates
   */
  @javax.annotation.Nonnull
  public List<LocalDate> getDates() {
    return dates;
  }

  public void setDates(@javax.annotation.Nonnull List<LocalDate> dates) {
    this.dates = dates;
  }


  public SpecialEvent price(@javax.annotation.Nonnull Float price) {
    this.price = price;
    return this;
  }

  /**
   * Price of a ticket for the special event.
   * @return price
   */
  @javax.annotation.Nonnull
  public Float getPrice() {
    return price;
  }

  public void setPrice(@javax.annotation.Nonnull Float price) {
    this.price = price;
  }



  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    SpecialEvent specialEvent = (SpecialEvent) o;
    return Objects.equals(this.eventId, specialEvent.eventId) &&
        Objects.equals(this.name, specialEvent.name) &&
        Objects.equals(this.location, specialEvent.location) &&
        Objects.equals(this.eventDescription, specialEvent.eventDescription) &&
        Objects.equals(this.dates, specialEvent.dates) &&
        Objects.equals(this.price, specialEvent.price);
  }

  @Override
  public int hashCode() {
    return Objects.hash(eventId, name, location, eventDescription, dates, price);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class SpecialEvent {\n");
    sb.append("    eventId: ").append(toIndentedString(eventId)).append("\n");
    sb.append("    name: ").append(toIndentedString(name)).append("\n");
    sb.append("    location: ").append(toIndentedString(location)).append("\n");
    sb.append("    eventDescription: ").append(toIndentedString(eventDescription)).append("\n");
    sb.append("    dates: ").append(toIndentedString(dates)).append("\n");
    sb.append("    price: ").append(toIndentedString(price)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }


  public static HashSet<String> openapiFields;
  public static HashSet<String> openapiRequiredFields;

  static {
    // a set of all properties/fields (JSON key names)
    openapiFields = new HashSet<String>();
    openapiFields.add("eventId");
    openapiFields.add("name");
    openapiFields.add("location");
    openapiFields.add("eventDescription");
    openapiFields.add("dates");
    openapiFields.add("price");

    // a set of required properties/fields (JSON key names)
    openapiRequiredFields = new HashSet<String>();
    openapiRequiredFields.add("name");
    openapiRequiredFields.add("location");
    openapiRequiredFields.add("eventDescription");
    openapiRequiredFields.add("dates");
    openapiRequiredFields.add("price");
  }

  /**
   * Validates the JSON Element and throws an exception if issues found
   *
   * @param jsonElement JSON Element
   * @throws IOException if the JSON Element is invalid with respect to SpecialEvent
   */
  public static void validateJsonElement(JsonElement jsonElement) throws IOException {
      if (jsonElement == null) {
        if (!SpecialEvent.openapiRequiredFields.isEmpty()) { // has required fields but JSON element is null
          throw new IllegalArgumentException(String.format("The required field(s) %s in SpecialEvent is not found in the empty JSON string", SpecialEvent.openapiRequiredFields.toString()));
        }
      }

      Set<Map.Entry<String, JsonElement>> entries = jsonElement.getAsJsonObject().entrySet();
      // check to see if the JSON string contains additional fields
      for (Map.Entry<String, JsonElement> entry : entries) {
        if (!SpecialEvent.openapiFields.contains(entry.getKey())) {
          throw new IllegalArgumentException(String.format("The field `%s` in the JSON string is not defined in the `SpecialEvent` properties. JSON: %s", entry.getKey(), jsonElement.toString()));
        }
      }

      // check to make sure all required properties/fields are present in the JSON string
      for (String requiredField : SpecialEvent.openapiRequiredFields) {
        if (jsonElement.getAsJsonObject().get(requiredField) == null) {
          throw new IllegalArgumentException(String.format("The required field `%s` is not found in the JSON string: %s", requiredField, jsonElement.toString()));
        }
      }
        JsonObject jsonObj = jsonElement.getAsJsonObject();
      if ((jsonObj.get("eventId") != null && !jsonObj.get("eventId").isJsonNull()) && !jsonObj.get("eventId").isJsonPrimitive()) {
        throw new IllegalArgumentException(String.format("Expected the field `eventId` to be a primitive type in the JSON string but got `%s`", jsonObj.get("eventId").toString()));
      }
      if (!jsonObj.get("name").isJsonPrimitive()) {
        throw new IllegalArgumentException(String.format("Expected the field `name` to be a primitive type in the JSON string but got `%s`", jsonObj.get("name").toString()));
      }
      if (!jsonObj.get("location").isJsonPrimitive()) {
        throw new IllegalArgumentException(String.format("Expected the field `location` to be a primitive type in the JSON string but got `%s`", jsonObj.get("location").toString()));
      }
      if (!jsonObj.get("eventDescription").isJsonPrimitive()) {
        throw new IllegalArgumentException(String.format("Expected the field `eventDescription` to be a primitive type in the JSON string but got `%s`", jsonObj.get("eventDescription").toString()));
      }
      // ensure the required json array is present
      if (jsonObj.get("dates") == null) {
        throw new IllegalArgumentException("Expected the field `linkedContent` to be an array in the JSON string but got `null`");
      } else if (!jsonObj.get("dates").isJsonArray()) {
        throw new IllegalArgumentException(String.format("Expected the field `dates` to be an array in the JSON string but got `%s`", jsonObj.get("dates").toString()));
      }
  }

  public static class CustomTypeAdapterFactory implements TypeAdapterFactory {
    @SuppressWarnings("unchecked")
    @Override
    public <T> TypeAdapter<T> create(Gson gson, TypeToken<T> type) {
       if (!SpecialEvent.class.isAssignableFrom(type.getRawType())) {
         return null; // this class only serializes 'SpecialEvent' and its subtypes
       }
       final TypeAdapter<JsonElement> elementAdapter = gson.getAdapter(JsonElement.class);
       final TypeAdapter<SpecialEvent> thisAdapter
                        = gson.getDelegateAdapter(this, TypeToken.get(SpecialEvent.class));

       return (TypeAdapter<T>) new TypeAdapter<SpecialEvent>() {
           @Override
           public void write(JsonWriter out, SpecialEvent value) throws IOException {
             JsonObject obj = thisAdapter.toJsonTree(value).getAsJsonObject();
             elementAdapter.write(out, obj);
           }

           @Override
           public SpecialEvent read(JsonReader in) throws IOException {
             JsonElement jsonElement = elementAdapter.read(in);
             validateJsonElement(jsonElement);
             return thisAdapter.fromJsonTree(jsonElement);
           }

       }.nullSafe();
    }
  }

  /**
   * Create an instance of SpecialEvent given an JSON string
   *
   * @param jsonString JSON string
   * @return An instance of SpecialEvent
   * @throws IOException if the JSON string is invalid with respect to SpecialEvent
   */
  public static SpecialEvent fromJson(String jsonString) throws IOException {
    return JSON.getGson().fromJson(jsonString, SpecialEvent.class);
  }

  /**
   * Convert an instance of SpecialEvent to an JSON string
   *
   * @return JSON string
   */
  public String toJson() {
    return JSON.getGson().toJson(this);
  }
}

