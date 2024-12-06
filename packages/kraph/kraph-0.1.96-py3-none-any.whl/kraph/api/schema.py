from kraph.traits import (
    GraphTrait,
    ExpressionTrait,
    HasPresignedDownloadAccessor,
    OntologyTrait,
    LinkedExpressionTrait,
    EntityTrait,
    EntityRelationTrait,
)
from rath.scalars import ID
from kraph.scalars import RemoteUpload
from pydantic import ConfigDict, BaseModel, Field
from kraph.rath import KraphRath
from typing import Optional, Tuple, Literal, Any, List
from kraph.funcs import aexecute, execute
from enum import Enum
from datetime import datetime


class ExpressionKind(str, Enum):
    STRUCTURE = "STRUCTURE"
    MEASUREMENT = "MEASUREMENT"
    RELATION = "RELATION"
    ENTITY = "ENTITY"
    METRIC = "METRIC"
    RELATION_METRIC = "RELATION_METRIC"
    CONCEPT = "CONCEPT"


class MetricDataType(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    DATETIME = "DATETIME"
    STRING = "STRING"
    CATEGORY = "CATEGORY"
    BOOLEAN = "BOOLEAN"
    THREE_D_VECTOR = "THREE_D_VECTOR"
    TWO_D_VECTOR = "TWO_D_VECTOR"
    ONE_D_VECTOR = "ONE_D_VECTOR"
    FOUR_D_VECTOR = "FOUR_D_VECTOR"
    N_VECTOR = "N_VECTOR"


class LinkedExpressionFilter(BaseModel):
    graph: Optional[ID] = None
    search: Optional[str] = None
    pinned: Optional[bool] = None
    kind: Optional[ExpressionKind] = None
    ids: Optional[Tuple[ID, ...]] = None
    and_: Optional["LinkedExpressionFilter"] = Field(alias="AND", default=None)
    or_: Optional["LinkedExpressionFilter"] = Field(alias="OR", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OffsetPaginationInput(BaseModel):
    offset: int
    limit: int
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityFilter(BaseModel):
    graph: Optional[ID] = None
    kind: Optional[ID] = None
    ids: Optional[Tuple[ID, ...]] = None
    linked_expression: Optional[ID] = Field(alias="linkedExpression", default=None)
    identifier: Optional[str] = None
    object: Optional[ID] = None
    search: Optional[str] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphPaginationInput(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityRelationFilter(BaseModel):
    graph: Optional[ID] = None
    kind: Optional[ID] = None
    ids: Optional[Tuple[ID, ...]] = None
    linked_expression: Optional[ID] = Field(alias="linkedExpression", default=None)
    search: Optional[str] = None
    with_self: Optional[bool] = Field(alias="withSelf", default=None)
    left_id: Optional[ID] = Field(alias="leftId", default=None)
    right_id: Optional[ID] = Field(alias="rightId", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureRelationInput(BaseModel):
    left: "Structure"
    right: "Structure"
    kind: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class Structure(BaseModel):
    identifier: str
    id: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ProtocolStepInput(BaseModel):
    template: ID
    entity: ID
    reagent_mappings: Tuple["ReagentMappingInput", ...] = Field(alias="reagentMappings")
    value_mappings: Tuple["VariableInput", ...] = Field(alias="valueMappings")
    performed_at: Optional[datetime] = Field(alias="performedAt", default=None)
    performed_by: Optional[ID] = Field(alias="performedBy", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ReagentMappingInput(BaseModel):
    reagent: ID
    volume: int
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class VariableInput(BaseModel):
    key: str
    value: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class LinkedExpressionGraph(GraphTrait, BaseModel):
    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class LinkedExpressionExpressionOntology(OntologyTrait, BaseModel):
    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class LinkedExpressionExpression(ExpressionTrait, BaseModel):
    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    label: str
    ontology: LinkedExpressionExpressionOntology
    model_config = ConfigDict(frozen=True)


class LinkedExpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    graph: LinkedExpressionGraph
    kind: ExpressionKind
    expression: LinkedExpressionExpression
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionGraph(GraphTrait, BaseModel):
    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionExpressionOntology(OntologyTrait, BaseModel):
    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionExpression(ExpressionTrait, BaseModel):
    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    label: str
    ontology: ListLinkedExpressionExpressionOntology
    model_config = ConfigDict(frozen=True)


class ListLinkedExpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    graph: ListLinkedExpressionGraph
    kind: ExpressionKind
    expression: ListLinkedExpressionExpression
    model_config = ConfigDict(frozen=True)


class PresignedPostCredentials(BaseModel):
    typename: Literal["PresignedPostCredentials"] = Field(
        alias="__typename", default="PresignedPostCredentials", exclude=True
    )
    key: str
    x_amz_credential: str = Field(alias="xAmzCredential")
    x_amz_algorithm: str = Field(alias="xAmzAlgorithm")
    x_amz_date: str = Field(alias="xAmzDate")
    x_amz_signature: str = Field(alias="xAmzSignature")
    policy: str
    datalayer: str
    bucket: str
    store: str
    model_config = ConfigDict(frozen=True)


class Graph(GraphTrait, BaseModel):
    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepTemplate(BaseModel):
    typename: Literal["ProtocolStepTemplate"] = Field(
        alias="__typename", default="ProtocolStepTemplate", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappingsReagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappings(BaseModel):
    typename: Literal["ReagentMapping"] = Field(
        alias="__typename", default="ReagentMapping", exclude=True
    )
    reagent: ProtocolStepReagentmappingsReagent
    model_config = ConfigDict(frozen=True)


class ProtocolStepForreagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStep(BaseModel):
    typename: Literal["ProtocolStep"] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    id: ID
    template: ProtocolStepTemplate
    reagent_mappings: Tuple[ProtocolStepReagentmappings, ...] = Field(
        alias="reagentMappings"
    )
    for_reagent: Optional[ProtocolStepForreagent] = Field(
        default=None, alias="forReagent"
    )
    model_config = ConfigDict(frozen=True)


class ExpressionOntology(OntologyTrait, BaseModel):
    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class Expression(ExpressionTrait, BaseModel):
    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    label: str
    ontology: ExpressionOntology
    model_config = ConfigDict(frozen=True)


class EntityRelationLeft(EntityTrait, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelationRight(EntityTrait, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelationLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelation(EntityRelationTrait, BaseModel):
    typename: Literal["EntityRelation"] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    id: ID
    left: EntityRelationLeft
    right: EntityRelationRight
    linked_expression: EntityRelationLinkedexpression = Field(alias="linkedExpression")
    model_config = ConfigDict(frozen=True)


class ReagentExpression(ExpressionTrait, BaseModel):
    typename: Literal["Expression"] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class Reagent(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    expression: Optional[ReagentExpression] = Field(default=None)
    lot_id: str = Field(alias="lotId")
    model_config = ConfigDict(frozen=True)


class EntityLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    label: str
    model_config = ConfigDict(frozen=True)


class Entity(EntityTrait, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    label: str
    linked_expression: EntityLinkedexpression = Field(alias="linkedExpression")
    model_config = ConfigDict(frozen=True)


class ListEntityLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    label: str
    kind: ExpressionKind
    model_config = ConfigDict(frozen=True)


class ListEntity(EntityTrait, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    label: str
    linked_expression: ListEntityLinkedexpression = Field(alias="linkedExpression")
    object: Optional[str] = Field(default=None)
    identifier: Optional[str] = Field(default=None)
    model_config = ConfigDict(frozen=True)


class Ontology(OntologyTrait, BaseModel):
    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class MediaStore(HasPresignedDownloadAccessor, BaseModel):
    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    id: ID
    presigned_url: str = Field(alias="presignedUrl")
    key: str
    model_config = ConfigDict(frozen=True)


class Model(BaseModel):
    typename: Literal["Model"] = Field(
        alias="__typename", default="Model", exclude=True
    )
    id: ID
    name: str
    store: Optional[MediaStore] = Field(default=None)
    model_config = ConfigDict(frozen=True)


class LinkExpressionMutation(BaseModel):
    link_expression: LinkedExpression = Field(alias="linkExpression")

    class Arguments(BaseModel):
        expression: ID
        graph: ID

    class Meta:
        document = "fragment LinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n    __typename\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation LinkExpression($expression: ID!, $graph: ID!) {\n  linkExpression(input: {expression: $expression, graph: $graph}) {\n    ...LinkedExpression\n    __typename\n  }\n}"


class CreateModelMutation(BaseModel):
    create_model: Model = Field(alias="createModel")

    class Arguments(BaseModel):
        model: RemoteUpload
        name: str

    class Meta:
        document = "fragment MediaStore on MediaStore {\n  id\n  presignedUrl\n  key\n  __typename\n}\n\nfragment Model on Model {\n  id\n  name\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nmutation CreateModel($model: RemoteUpload!, $name: String!) {\n  createModel(input: {name: $name, model: $model}) {\n    ...Model\n    __typename\n  }\n}"


class CreateGraphMutation(BaseModel):
    create_graph: Graph = Field(alias="createGraph")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n  __typename\n}\n\nmutation CreateGraph($name: String!) {\n  createGraph(input: {name: $name}) {\n    ...Graph\n    __typename\n  }\n}"


class RequestUploadMutation(BaseModel):
    request_upload: PresignedPostCredentials = Field(alias="requestUpload")

    class Arguments(BaseModel):
        key: str
        datalayer: str

    class Meta:
        document = "fragment PresignedPostCredentials on PresignedPostCredentials {\n  key\n  xAmzCredential\n  xAmzAlgorithm\n  xAmzDate\n  xAmzSignature\n  policy\n  datalayer\n  bucket\n  store\n  __typename\n}\n\nmutation RequestUpload($key: String!, $datalayer: String!) {\n  requestUpload(input: {key: $key, datalayer: $datalayer}) {\n    ...PresignedPostCredentials\n    __typename\n  }\n}"


class CreateProtocolStepMutation(BaseModel):
    create_protocol_step: ProtocolStep = Field(alias="createProtocolStep")

    class Arguments(BaseModel):
        input: ProtocolStepInput

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n    __typename\n  }\n  reagentMappings {\n    reagent {\n      id\n      __typename\n    }\n    __typename\n  }\n  forReagent {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateProtocolStep($input: ProtocolStepInput!) {\n  createProtocolStep(input: $input) {\n    ...ProtocolStep\n    __typename\n  }\n}"


class CreateExpressionMutation(BaseModel):
    create_expression: Expression = Field(alias="createExpression")

    class Arguments(BaseModel):
        label: str
        ontology: Optional[ID] = Field(default=None)
        purl: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)
        color: Optional[List[int]] = Field(default=None)
        metric_kind: Optional[MetricDataType] = Field(alias="metricKind", default=None)
        kind: ExpressionKind

    class Meta:
        document = "fragment Expression on Expression {\n  id\n  label\n  ontology {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation CreateExpression($label: String!, $ontology: ID, $purl: String, $description: String, $color: [Int!], $metricKind: MetricDataType, $kind: ExpressionKind!) {\n  createExpression(\n    input: {label: $label, ontology: $ontology, description: $description, purl: $purl, color: $color, kind: $kind, metricKind: $metricKind}\n  ) {\n    ...Expression\n    __typename\n  }\n}"


class CreateEntityRelationMutation(BaseModel):
    create_entity_relation: EntityRelation = Field(alias="createEntityRelation")

    class Arguments(BaseModel):
        left: ID
        right: ID
        kind: ID

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntityRelation($left: ID!, $right: ID!, $kind: ID!) {\n  createEntityRelation(input: {left: $left, right: $right, kind: $kind}) {\n    ...EntityRelation\n    __typename\n  }\n}"


class CreateRoiEntityRelationMutation(BaseModel):
    create_structure_relation: EntityRelation = Field(alias="createStructureRelation")

    class Arguments(BaseModel):
        input: StructureRelationInput

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRoiEntityRelation($input: StructureRelationInput!) {\n  createStructureRelation(input: $input) {\n    ...EntityRelation\n    __typename\n  }\n}"


class CreateReagentMutation(BaseModel):
    create_reagent: Reagent = Field(alias="createReagent")

    class Arguments(BaseModel):
        expression: ID
        lot_id: str = Field(alias="lotId")

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n    __typename\n  }\n  lotId\n  __typename\n}\n\nmutation CreateReagent($expression: ID!, $lotId: String!) {\n  createReagent(input: {expression: $expression, lotId: $lotId}) {\n    ...Reagent\n    __typename\n  }\n}"


class CreateEntityMetricMutation(BaseModel):
    create_entity_metric: Entity = Field(alias="createEntityMetric")

    class Arguments(BaseModel):
        entity: ID
        metric: ID
        value: Any
        timepoint: Optional[datetime] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntityMetric($entity: ID!, $metric: ID!, $value: Metric!, $timepoint: DateTime) {\n  createEntityMetric(\n    input: {entity: $entity, metric: $metric, value: $value, timepoint: $timepoint}\n  ) {\n    ...Entity\n    __typename\n  }\n}"


class CreateRelationMetricMutation(BaseModel):
    create_relation_metric: EntityRelation = Field(alias="createRelationMetric")

    class Arguments(BaseModel):
        relation: ID
        metric: ID
        value: Any
        timepoint: Optional[datetime] = Field(default=None)

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRelationMetric($relation: ID!, $metric: ID!, $value: Metric!, $timepoint: DateTime) {\n  createRelationMetric(\n    input: {relation: $relation, metric: $metric, value: $value, timepoint: $timepoint}\n  ) {\n    ...EntityRelation\n    __typename\n  }\n}"


class CreateEntityMutation(BaseModel):
    create_entity: Entity = Field(alias="createEntity")

    class Arguments(BaseModel):
        kind: ID
        group: Optional[ID] = Field(default=None)
        name: Optional[str] = Field(default=None)
        parent: Optional[ID] = Field(default=None)
        instance_kind: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntity($kind: ID!, $group: ID, $name: String, $parent: ID, $instance_kind: String) {\n  createEntity(\n    input: {group: $group, kind: $kind, name: $name, parent: $parent, instanceKind: $instance_kind}\n  ) {\n    ...Entity\n    __typename\n  }\n}"


class CreateMeasurementMutation(BaseModel):
    create_measurement: Entity = Field(alias="createMeasurement")

    class Arguments(BaseModel):
        structure: str
        graph: ID

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMeasurement($structure: StructureString!, $graph: ID!) {\n  createMeasurement(input: {structure: $structure, graph: $graph}) {\n    ...Entity\n    __typename\n  }\n}"


class CreateOntologyMutation(BaseModel):
    create_ontology: Ontology = Field(alias="createOntology")

    class Arguments(BaseModel):
        name: str
        purl: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Ontology on Ontology {\n  id\n  name\n  __typename\n}\n\nmutation CreateOntology($name: String!, $purl: String, $description: String) {\n  createOntology(input: {name: $name, purl: $purl, description: $description}) {\n    ...Ontology\n    __typename\n  }\n}"


class GetLinkedExpressionQuery(BaseModel):
    linked_expression: LinkedExpression = Field(alias="linkedExpression")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment LinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n    __typename\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetLinkedExpression($id: ID!) {\n  linkedExpression(id: $id) {\n    ...LinkedExpression\n    __typename\n  }\n}"


class SearchLinkedExpressionsQueryOptions(LinkedExpressionTrait, BaseModel):
    typename: Literal["LinkedExpression"] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchLinkedExpressionsQuery(BaseModel):
    options: Tuple[SearchLinkedExpressionsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchLinkedExpressions($search: String, $values: [ID!]) {\n  options: linkedExpressions(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class ListLinkedExpressionsQuery(BaseModel):
    linked_expressions: Tuple[ListLinkedExpression, ...] = Field(
        alias="linkedExpressions"
    )

    class Arguments(BaseModel):
        filters: Optional[LinkedExpressionFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment ListLinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n    __typename\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery ListLinkedExpressions($filters: LinkedExpressionFilter, $pagination: OffsetPaginationInput) {\n  linkedExpressions(filters: $filters, pagination: $pagination) {\n    ...ListLinkedExpression\n    __typename\n  }\n}"


class GetModelQuery(BaseModel):
    model: Model

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment MediaStore on MediaStore {\n  id\n  presignedUrl\n  key\n  __typename\n}\n\nfragment Model on Model {\n  id\n  name\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nquery GetModel($id: ID!) {\n  model(id: $id) {\n    ...Model\n    __typename\n  }\n}"


class SearchModelsQueryOptions(BaseModel):
    typename: Literal["Model"] = Field(
        alias="__typename", default="Model", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchModelsQuery(BaseModel):
    options: Tuple[SearchModelsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchModels($search: String, $values: [ID!]) {\n  options: models(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetGraphQuery(BaseModel):
    graph: Graph

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n  __typename\n}\n\nquery GetGraph($id: ID!) {\n  graph(id: $id) {\n    ...Graph\n    __typename\n  }\n}"


class SearchGraphsQueryOptions(GraphTrait, BaseModel):
    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchGraphsQuery(BaseModel):
    options: Tuple[SearchGraphsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGraphs($search: String, $values: [ID!]) {\n  options: graphs(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetProtocolStepQuery(BaseModel):
    protocol_step: ProtocolStep = Field(alias="protocolStep")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n    __typename\n  }\n  reagentMappings {\n    reagent {\n      id\n      __typename\n    }\n    __typename\n  }\n  forReagent {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetProtocolStep($id: ID!) {\n  protocolStep(id: $id) {\n    ...ProtocolStep\n    __typename\n  }\n}"


class SearchProtocolStepsQueryOptions(BaseModel):
    typename: Literal["ProtocolStep"] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchProtocolStepsQuery(BaseModel):
    options: Tuple[SearchProtocolStepsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchProtocolSteps($search: String, $values: [ID!]) {\n  options: protocolSteps(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetEntityRelationQuery(BaseModel):
    entity_relation: EntityRelation = Field(alias="entityRelation")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n    __typename\n  }\n  right {\n    id\n    __typename\n  }\n  linkedExpression {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetEntityRelation($id: ID!) {\n  entityRelation(id: $id) {\n    ...EntityRelation\n    __typename\n  }\n}"


class SearchEntityRelationsQueryOptions(EntityRelationTrait, BaseModel):
    typename: Literal["EntityRelation"] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchEntityRelationsQuery(BaseModel):
    options: Tuple[SearchEntityRelationsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntityRelations($search: String, $values: [ID!]) {\n  options: entityRelations(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetReagentQuery(BaseModel):
    reagent: Reagent

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n    __typename\n  }\n  lotId\n  __typename\n}\n\nquery GetReagent($id: ID!) {\n  reagent(id: $id) {\n    ...Reagent\n    __typename\n  }\n}"


class SearchReagentsQueryOptions(BaseModel):
    typename: Literal["Reagent"] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchReagentsQuery(BaseModel):
    options: Tuple[SearchReagentsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchReagents($search: String, $values: [ID!]) {\n  options: reagents(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetEntityQuery(BaseModel):
    entity: Entity

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nquery GetEntity($id: ID!) {\n  entity(id: $id) {\n    ...Entity\n    __typename\n  }\n}"


class SearchEntitiesQueryOptions(EntityTrait, BaseModel):
    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchEntitiesQuery(BaseModel):
    options: Tuple[SearchEntitiesQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntities($search: String, $values: [ID!]) {\n  options: entities(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class EntitiesQuery(BaseModel):
    entities: Tuple[Entity, ...]

    class Arguments(BaseModel):
        filters: Optional[EntityFilter] = Field(default=None)
        pagination: Optional[GraphPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nquery Entities($filters: EntityFilter, $pagination: GraphPaginationInput) {\n  entities(filters: $filters, pagination: $pagination) {\n    ...Entity\n    __typename\n  }\n}"


class ListPairedEntitiesQueryPairedentitiesRelation(EntityRelationTrait, BaseModel):
    typename: Literal["EntityRelation"] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    id: ID
    label: str
    model_config = ConfigDict(frozen=True)


class ListPairedEntitiesQueryPairedentities(BaseModel):
    typename: Literal["PairedStructure"] = Field(
        alias="__typename", default="PairedStructure", exclude=True
    )
    left: ListEntity
    right: ListEntity
    relation: ListPairedEntitiesQueryPairedentitiesRelation
    model_config = ConfigDict(frozen=True)


class ListPairedEntitiesQuery(BaseModel):
    paired_entities: Tuple[ListPairedEntitiesQueryPairedentities, ...] = Field(
        alias="pairedEntities"
    )

    class Arguments(BaseModel):
        graph: ID
        relation_filter: Optional[EntityRelationFilter] = Field(
            alias="relationFilter", default=None
        )
        left_filter: Optional[EntityFilter] = Field(alias="leftFilter", default=None)
        right_filter: Optional[EntityFilter] = Field(alias="rightFilter", default=None)
        pagination: Optional[GraphPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment ListEntity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n    kind\n    __typename\n  }\n  object\n  identifier\n  __typename\n}\n\nquery ListPairedEntities($graph: ID!, $relationFilter: EntityRelationFilter, $leftFilter: EntityFilter, $rightFilter: EntityFilter, $pagination: GraphPaginationInput) {\n  pairedEntities(\n    graph: $graph\n    rightFilter: $rightFilter\n    pagination: $pagination\n    leftFilter: $leftFilter\n    relationFilter: $relationFilter\n  ) {\n    left {\n      ...ListEntity\n      __typename\n    }\n    right {\n      ...ListEntity\n      __typename\n    }\n    relation {\n      id\n      label\n      __typename\n    }\n    __typename\n  }\n}"


class GetOntologyQuery(BaseModel):
    ontology: Ontology

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Ontology on Ontology {\n  id\n  name\n  __typename\n}\n\nquery GetOntology($id: ID!) {\n  ontology(id: $id) {\n    ...Ontology\n    __typename\n  }\n}"


class SearchOntologiesQueryOptions(OntologyTrait, BaseModel):
    typename: Literal["Ontology"] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchOntologiesQuery(BaseModel):
    options: Tuple[SearchOntologiesQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchOntologies($search: String, $values: [ID!]) {\n  options: ontologies(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


async def alink_expression(
    expression: ID, graph: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """LinkExpression



    Arguments:
        expression (ID): expression
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkExpressionMutationLinkexpression"""
    return (
        await aexecute(
            LinkExpressionMutation,
            {"expression": expression, "graph": graph},
            rath=rath,
        )
    ).link_expression


def link_expression(
    expression: ID, graph: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """LinkExpression



    Arguments:
        expression (ID): expression
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkExpressionMutationLinkexpression"""
    return execute(
        LinkExpressionMutation, {"expression": expression, "graph": graph}, rath=rath
    ).link_expression


async def acreate_model(
    model: RemoteUpload, name: str, rath: Optional[KraphRath] = None
) -> Model:
    """CreateModel



    Arguments:
        model (RemoteUpload): model
        name (str): name
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateModelMutationCreatemodel"""
    return (
        await aexecute(CreateModelMutation, {"model": model, "name": name}, rath=rath)
    ).create_model


def create_model(
    model: RemoteUpload, name: str, rath: Optional[KraphRath] = None
) -> Model:
    """CreateModel



    Arguments:
        model (RemoteUpload): model
        name (str): name
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateModelMutationCreatemodel"""
    return execute(
        CreateModelMutation, {"model": model, "name": name}, rath=rath
    ).create_model


async def acreate_graph(name: str, rath: Optional[KraphRath] = None) -> Graph:
    """CreateGraph



    Arguments:
        name (str): name
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateGraphMutationCreategraph"""
    return (await aexecute(CreateGraphMutation, {"name": name}, rath=rath)).create_graph


def create_graph(name: str, rath: Optional[KraphRath] = None) -> Graph:
    """CreateGraph



    Arguments:
        name (str): name
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateGraphMutationCreategraph"""
    return execute(CreateGraphMutation, {"name": name}, rath=rath).create_graph


async def arequest_upload(
    key: str, datalayer: str, rath: Optional[KraphRath] = None
) -> PresignedPostCredentials:
    """RequestUpload


     requestUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        RequestUploadMutationRequestupload"""
    return (
        await aexecute(
            RequestUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
        )
    ).request_upload


def request_upload(
    key: str, datalayer: str, rath: Optional[KraphRath] = None
) -> PresignedPostCredentials:
    """RequestUpload


     requestUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        RequestUploadMutationRequestupload"""
    return execute(
        RequestUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
    ).request_upload


async def acreate_protocol_step(
    input: ProtocolStepInput, rath: Optional[KraphRath] = None
) -> ProtocolStep:
    """CreateProtocolStep



    Arguments:
        input (ProtocolStepInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateProtocolStepMutationCreateprotocolstep"""
    return (
        await aexecute(CreateProtocolStepMutation, {"input": input}, rath=rath)
    ).create_protocol_step


def create_protocol_step(
    input: ProtocolStepInput, rath: Optional[KraphRath] = None
) -> ProtocolStep:
    """CreateProtocolStep



    Arguments:
        input (ProtocolStepInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateProtocolStepMutationCreateprotocolstep"""
    return execute(
        CreateProtocolStepMutation, {"input": input}, rath=rath
    ).create_protocol_step


async def acreate_expression(
    label: str,
    kind: ExpressionKind,
    ontology: Optional[ID] = None,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[List[int]] = None,
    metric_kind: Optional[MetricDataType] = None,
    rath: Optional[KraphRath] = None,
) -> Expression:
    """CreateExpression



    Arguments:
        label (str): label
        kind (ExpressionKind): kind
        ontology (Optional[ID], optional): ontology.
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        color (Optional[List[int]], optional): color.
        metric_kind (Optional[MetricDataType], optional): metricKind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateExpressionMutationCreateexpression"""
    return (
        await aexecute(
            CreateExpressionMutation,
            {
                "label": label,
                "ontology": ontology,
                "purl": purl,
                "description": description,
                "color": color,
                "metricKind": metric_kind,
                "kind": kind,
            },
            rath=rath,
        )
    ).create_expression


def create_expression(
    label: str,
    kind: ExpressionKind,
    ontology: Optional[ID] = None,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[List[int]] = None,
    metric_kind: Optional[MetricDataType] = None,
    rath: Optional[KraphRath] = None,
) -> Expression:
    """CreateExpression



    Arguments:
        label (str): label
        kind (ExpressionKind): kind
        ontology (Optional[ID], optional): ontology.
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        color (Optional[List[int]], optional): color.
        metric_kind (Optional[MetricDataType], optional): metricKind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateExpressionMutationCreateexpression"""
    return execute(
        CreateExpressionMutation,
        {
            "label": label,
            "ontology": ontology,
            "purl": purl,
            "description": description,
            "color": color,
            "metricKind": metric_kind,
            "kind": kind,
        },
        rath=rath,
    ).create_expression


async def acreate_entity_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateEntityRelation



    Arguments:
        left (ID): left
        right (ID): right
        kind (ID): kind
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateEntityRelationMutationCreateentityrelation"""
    return (
        await aexecute(
            CreateEntityRelationMutation,
            {"left": left, "right": right, "kind": kind},
            rath=rath,
        )
    ).create_entity_relation


def create_entity_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateEntityRelation



    Arguments:
        left (ID): left
        right (ID): right
        kind (ID): kind
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateEntityRelationMutationCreateentityrelation"""
    return execute(
        CreateEntityRelationMutation,
        {"left": left, "right": right, "kind": kind},
        rath=rath,
    ).create_entity_relation


async def acreate_roi_entity_relation(
    input: StructureRelationInput, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateRoiEntityRelation



    Arguments:
        input (StructureRelationInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateRoiEntityRelationMutationCreatestructurerelation"""
    return (
        await aexecute(CreateRoiEntityRelationMutation, {"input": input}, rath=rath)
    ).create_structure_relation


def create_roi_entity_relation(
    input: StructureRelationInput, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateRoiEntityRelation



    Arguments:
        input (StructureRelationInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateRoiEntityRelationMutationCreatestructurerelation"""
    return execute(
        CreateRoiEntityRelationMutation, {"input": input}, rath=rath
    ).create_structure_relation


async def acreate_reagent(
    expression: ID, lot_id: str, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent



    Arguments:
        expression (ID): expression
        lot_id (str): lotId
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateReagentMutationCreatereagent"""
    return (
        await aexecute(
            CreateReagentMutation,
            {"expression": expression, "lotId": lot_id},
            rath=rath,
        )
    ).create_reagent


def create_reagent(
    expression: ID, lot_id: str, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent



    Arguments:
        expression (ID): expression
        lot_id (str): lotId
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateReagentMutationCreatereagent"""
    return execute(
        CreateReagentMutation, {"expression": expression, "lotId": lot_id}, rath=rath
    ).create_reagent


async def acreate_entity_metric(
    entity: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntityMetric



    Arguments:
        entity (ID): entity
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateEntityMetricMutationCreateentitymetric"""
    return (
        await aexecute(
            CreateEntityMetricMutation,
            {
                "entity": entity,
                "metric": metric,
                "value": value,
                "timepoint": timepoint,
            },
            rath=rath,
        )
    ).create_entity_metric


def create_entity_metric(
    entity: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntityMetric



    Arguments:
        entity (ID): entity
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateEntityMetricMutationCreateentitymetric"""
    return execute(
        CreateEntityMetricMutation,
        {"entity": entity, "metric": metric, "value": value, "timepoint": timepoint},
        rath=rath,
    ).create_entity_metric


async def acreate_relation_metric(
    relation: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> EntityRelation:
    """CreateRelationMetric



    Arguments:
        relation (ID): relation
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateRelationMetricMutationCreaterelationmetric"""
    return (
        await aexecute(
            CreateRelationMetricMutation,
            {
                "relation": relation,
                "metric": metric,
                "value": value,
                "timepoint": timepoint,
            },
            rath=rath,
        )
    ).create_relation_metric


def create_relation_metric(
    relation: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> EntityRelation:
    """CreateRelationMetric



    Arguments:
        relation (ID): relation
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateRelationMetricMutationCreaterelationmetric"""
    return execute(
        CreateRelationMetricMutation,
        {
            "relation": relation,
            "metric": metric,
            "value": value,
            "timepoint": timepoint,
        },
        rath=rath,
    ).create_relation_metric


async def acreate_entity(
    kind: ID,
    group: Optional[ID] = None,
    name: Optional[str] = None,
    parent: Optional[ID] = None,
    instance_kind: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity



    Arguments:
        kind (ID): kind
        group (Optional[ID], optional): group.
        name (Optional[str], optional): name.
        parent (Optional[ID], optional): parent.
        instance_kind (Optional[str], optional): instance_kind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateEntityMutationCreateentity"""
    return (
        await aexecute(
            CreateEntityMutation,
            {
                "kind": kind,
                "group": group,
                "name": name,
                "parent": parent,
                "instance_kind": instance_kind,
            },
            rath=rath,
        )
    ).create_entity


def create_entity(
    kind: ID,
    group: Optional[ID] = None,
    name: Optional[str] = None,
    parent: Optional[ID] = None,
    instance_kind: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity



    Arguments:
        kind (ID): kind
        group (Optional[ID], optional): group.
        name (Optional[str], optional): name.
        parent (Optional[ID], optional): parent.
        instance_kind (Optional[str], optional): instance_kind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateEntityMutationCreateentity"""
    return execute(
        CreateEntityMutation,
        {
            "kind": kind,
            "group": group,
            "name": name,
            "parent": parent,
            "instance_kind": instance_kind,
        },
        rath=rath,
    ).create_entity


async def acreate_measurement(
    structure: str, graph: ID, rath: Optional[KraphRath] = None
) -> Entity:
    """CreateMeasurement



    Arguments:
        structure (str): structure
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateMeasurementMutationCreatemeasurement"""
    return (
        await aexecute(
            CreateMeasurementMutation,
            {"structure": structure, "graph": graph},
            rath=rath,
        )
    ).create_measurement


def create_measurement(
    structure: str, graph: ID, rath: Optional[KraphRath] = None
) -> Entity:
    """CreateMeasurement



    Arguments:
        structure (str): structure
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateMeasurementMutationCreatemeasurement"""
    return execute(
        CreateMeasurementMutation, {"structure": structure, "graph": graph}, rath=rath
    ).create_measurement


async def acreate_ontology(
    name: str,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology



    Arguments:
        name (str): name
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateOntologyMutationCreateontology"""
    return (
        await aexecute(
            CreateOntologyMutation,
            {"name": name, "purl": purl, "description": description},
            rath=rath,
        )
    ).create_ontology


def create_ontology(
    name: str,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology



    Arguments:
        name (str): name
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        CreateOntologyMutationCreateontology"""
    return execute(
        CreateOntologyMutation,
        {"name": name, "purl": purl, "description": description},
        rath=rath,
    ).create_ontology


async def aget_linked_expression(
    id: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """GetLinkedExpression



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetLinkedExpressionQueryLinkedexpression"""
    return (
        await aexecute(GetLinkedExpressionQuery, {"id": id}, rath=rath)
    ).linked_expression


def get_linked_expression(id: ID, rath: Optional[KraphRath] = None) -> LinkedExpression:
    """GetLinkedExpression



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetLinkedExpressionQueryLinkedexpression"""
    return execute(GetLinkedExpressionQuery, {"id": id}, rath=rath).linked_expression


async def asearch_linked_expressions(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchLinkedExpressionsQueryOptions]:
    """SearchLinkedExpressions



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchLinkedExpressionsQueryLinkedexpressions]"""
    return (
        await aexecute(
            SearchLinkedExpressionsQuery,
            {"search": search, "values": values},
            rath=rath,
        )
    ).options


def search_linked_expressions(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchLinkedExpressionsQueryOptions]:
    """SearchLinkedExpressions



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchLinkedExpressionsQueryLinkedexpressions]"""
    return execute(
        SearchLinkedExpressionsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def alist_linked_expressions(
    filters: Optional[LinkedExpressionFilter] = None,
    pagination: Optional[OffsetPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListLinkedExpression]:
    """ListLinkedExpressions



    Arguments:
        filters (Optional[LinkedExpressionFilter], optional): filters.
        pagination (Optional[OffsetPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListLinkedExpressionsQueryLinkedexpressions]"""
    return (
        await aexecute(
            ListLinkedExpressionsQuery,
            {"filters": filters, "pagination": pagination},
            rath=rath,
        )
    ).linked_expressions


def list_linked_expressions(
    filters: Optional[LinkedExpressionFilter] = None,
    pagination: Optional[OffsetPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListLinkedExpression]:
    """ListLinkedExpressions



    Arguments:
        filters (Optional[LinkedExpressionFilter], optional): filters.
        pagination (Optional[OffsetPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListLinkedExpressionsQueryLinkedexpressions]"""
    return execute(
        ListLinkedExpressionsQuery,
        {"filters": filters, "pagination": pagination},
        rath=rath,
    ).linked_expressions


async def aget_model(id: ID, rath: Optional[KraphRath] = None) -> Model:
    """GetModel



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetModelQueryModel"""
    return (await aexecute(GetModelQuery, {"id": id}, rath=rath)).model


def get_model(id: ID, rath: Optional[KraphRath] = None) -> Model:
    """GetModel



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetModelQueryModel"""
    return execute(GetModelQuery, {"id": id}, rath=rath).model


async def asearch_models(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchModelsQueryOptions]:
    """SearchModels



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchModelsQueryModels]"""
    return (
        await aexecute(
            SearchModelsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_models(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchModelsQueryOptions]:
    """SearchModels



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchModelsQueryModels]"""
    return execute(
        SearchModelsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetGraphQueryGraph"""
    return (await aexecute(GetGraphQuery, {"id": id}, rath=rath)).graph


def get_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetGraphQueryGraph"""
    return execute(GetGraphQuery, {"id": id}, rath=rath).graph


async def asearch_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchGraphsQueryOptions]:
    """SearchGraphs



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return (
        await aexecute(
            SearchGraphsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchGraphsQueryOptions]:
    """SearchGraphs



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return execute(
        SearchGraphsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetProtocolStepQueryProtocolstep"""
    return (await aexecute(GetProtocolStepQuery, {"id": id}, rath=rath)).protocol_step


def get_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetProtocolStepQueryProtocolstep"""
    return execute(GetProtocolStepQuery, {"id": id}, rath=rath).protocol_step


async def asearch_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchProtocolStepsQueryOptions]:
    """SearchProtocolSteps



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return (
        await aexecute(
            SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchProtocolStepsQueryOptions]:
    """SearchProtocolSteps



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return execute(
        SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_entity_relation(
    id: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """GetEntityRelation



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetEntityRelationQueryEntityrelation"""
    return (
        await aexecute(GetEntityRelationQuery, {"id": id}, rath=rath)
    ).entity_relation


def get_entity_relation(id: ID, rath: Optional[KraphRath] = None) -> EntityRelation:
    """GetEntityRelation



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetEntityRelationQueryEntityrelation"""
    return execute(GetEntityRelationQuery, {"id": id}, rath=rath).entity_relation


async def asearch_entity_relations(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntityRelationsQueryOptions]:
    """SearchEntityRelations



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntityRelationsQueryEntityrelations]"""
    return (
        await aexecute(
            SearchEntityRelationsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entity_relations(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntityRelationsQueryOptions]:
    """SearchEntityRelations



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntityRelationsQueryEntityrelations]"""
    return execute(
        SearchEntityRelationsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetReagentQueryReagent"""
    return (await aexecute(GetReagentQuery, {"id": id}, rath=rath)).reagent


def get_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetReagentQueryReagent"""
    return execute(GetReagentQuery, {"id": id}, rath=rath).reagent


async def asearch_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchReagentsQueryOptions]:
    """SearchReagents



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return (
        await aexecute(
            SearchReagentsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchReagentsQueryOptions]:
    """SearchReagents



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return execute(
        SearchReagentsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_entity(id: ID, rath: Optional[KraphRath] = None) -> Entity:
    """GetEntity



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetEntityQueryEntity"""
    return (await aexecute(GetEntityQuery, {"id": id}, rath=rath)).entity


def get_entity(id: ID, rath: Optional[KraphRath] = None) -> Entity:
    """GetEntity



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetEntityQueryEntity"""
    return execute(GetEntityQuery, {"id": id}, rath=rath).entity


async def asearch_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntitiesQueryOptions]:
    """SearchEntities



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryEntities]"""
    return (
        await aexecute(
            SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntitiesQueryOptions]:
    """SearchEntities



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryEntities]"""
    return execute(
        SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aentities(
    filters: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[Entity]:
    """Entities



    Arguments:
        filters (Optional[EntityFilter], optional): filters.
        pagination (Optional[GraphPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[EntitiesQueryEntities]"""
    return (
        await aexecute(
            EntitiesQuery, {"filters": filters, "pagination": pagination}, rath=rath
        )
    ).entities


def entities(
    filters: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[Entity]:
    """Entities



    Arguments:
        filters (Optional[EntityFilter], optional): filters.
        pagination (Optional[GraphPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[EntitiesQueryEntities]"""
    return execute(
        EntitiesQuery, {"filters": filters, "pagination": pagination}, rath=rath
    ).entities


async def alist_paired_entities(
    graph: ID,
    relation_filter: Optional[EntityRelationFilter] = None,
    left_filter: Optional[EntityFilter] = None,
    right_filter: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListPairedEntitiesQueryPairedentities]:
    """ListPairedEntities



    Arguments:
        graph (ID): graph
        relation_filter (Optional[EntityRelationFilter], optional): relationFilter.
        left_filter (Optional[EntityFilter], optional): leftFilter.
        right_filter (Optional[EntityFilter], optional): rightFilter.
        pagination (Optional[GraphPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListPairedEntitiesQueryPairedentities]"""
    return (
        await aexecute(
            ListPairedEntitiesQuery,
            {
                "graph": graph,
                "relationFilter": relation_filter,
                "leftFilter": left_filter,
                "rightFilter": right_filter,
                "pagination": pagination,
            },
            rath=rath,
        )
    ).paired_entities


def list_paired_entities(
    graph: ID,
    relation_filter: Optional[EntityRelationFilter] = None,
    left_filter: Optional[EntityFilter] = None,
    right_filter: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListPairedEntitiesQueryPairedentities]:
    """ListPairedEntities



    Arguments:
        graph (ID): graph
        relation_filter (Optional[EntityRelationFilter], optional): relationFilter.
        left_filter (Optional[EntityFilter], optional): leftFilter.
        right_filter (Optional[EntityFilter], optional): rightFilter.
        pagination (Optional[GraphPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListPairedEntitiesQueryPairedentities]"""
    return execute(
        ListPairedEntitiesQuery,
        {
            "graph": graph,
            "relationFilter": relation_filter,
            "leftFilter": left_filter,
            "rightFilter": right_filter,
            "pagination": pagination,
        },
        rath=rath,
    ).paired_entities


async def aget_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetOntologyQueryOntology"""
    return (await aexecute(GetOntologyQuery, {"id": id}, rath=rath)).ontology


def get_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        GetOntologyQueryOntology"""
    return execute(GetOntologyQuery, {"id": id}, rath=rath).ontology


async def asearch_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchOntologiesQueryOptions]:
    """SearchOntologies



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return (
        await aexecute(
            SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchOntologiesQueryOptions]:
    """SearchOntologies



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return execute(
        SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
    ).options


LinkedExpressionFilter.model_rebuild()
ProtocolStepInput.model_rebuild()
StructureRelationInput.model_rebuild()
