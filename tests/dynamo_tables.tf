resource "aws_dynamodb_table" "change_in_condition" {
    name                     = "${var.environment}_change_in_condition"
    read_capacity            = "10"
    write_capacity           = "10"
    hash_key                 = "carelog_id"
    range_key                = "time"
    global_secondary_index {
      name            = "SavedInRDB"
      hash_key        = "saved_in_rdb"
      range_key       = "time"
      read_capacity   = "15"
      write_capacity  = "15"
      projection_type = "ALL"
    }
    global_secondary_index {
      name            = "AnotherIndex"
      hash_key        = "an_attribute"
      range_key       = "another_attribute"
      read_capacity   = "15"
      write_capacity  = "15"
      projection_type = "ALL"
    }
    local_secondary_index {
      name            = "SessionId"
      hash_key        = "carelog_id"
      range_key       = "session_id"
      projection_type = "ALL"
    }
    local_secondary_index {
      name            = "CaregiverId"
      hash_key        = "agency_id"
      range_key       = "caregiver_id"
      projection_type = "ALL"
    }
    attribute {
      name = "carelog_id"
      type = "N"
    }
    attribute {
      name = "time"
      type = "N"
    }
    attribute {
      name = "saved_in_rdb"
      type = "N"
    }
    attribute {
      name = "session_id"
      type = "N"
    }
    attribute {
      name = "an_attribute"
      type = "N"
    }
    attribute {
      name = "another_attribute"
      type = "N"
    }
    attribute {
      name = "agency_id"
      type = "N"
    }
    attribute {
      name = "caregiver_id"
      type = "N"
    }
}
