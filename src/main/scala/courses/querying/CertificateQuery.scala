package courses.querying

import util.Implicits._
import util.Data.using
import courses.DatabaseConfig

import com.mongodb.casbah.Imports._

import collection.immutable.ListMap

sealed abstract class CertificateQueryOption
case object StatusBreakdown extends CertificateQueryOption

object CertificateQuery {
    def apply(database: String) = new CertificateQuery(database)
}

class CertificateQuery(database: String) extends Query[CertificateQueryOption] {
    def of(query: CertificateQueryOption): QueryResult[String] = {
        query match {
            case StatusBreakdown =>
                using (database >> DatabaseConfig.CertificatesCollectionName) { certificatesCollection =>
                    val total = certificatesCollection.find()
                    val passing = certificatesCollection.find(MongoDBObject("status" -> "downloadable"), Query.UserIDField)
                    val notPassing = certificatesCollection.find(MongoDBObject("status" -> "notpassing"), Query.UserIDField)
                    val restricted = certificatesCollection.find(MongoDBObject("status" -> "restricted"), Query.UserIDField)
                    val unknown = certificatesCollection.find(
                        ("status" $ne "downloadable") ++ $and(("status" $ne "notpassing"), ("status" $ne "restricted")),
                        Query.UserIDField
                    )

                    QueryResult(Iterator(ListMap(
                        "total" -> total, 
                        "passing" -> passing, 
                        "notpassing" -> notPassing, 
                        "restricted" -> restricted, 
                        "unknown" -> unknown)))
                }
        }
    }
}